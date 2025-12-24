"""
QA Global Automation Coverage Dashboard
Main application file
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime

from modules.config import get_bu_names, get_bu_config
from modules.connector import fetch_data_recursive, validate_credentials
from modules.transformer import process
from modules.metrics import (
    calculate_overall_metrics,
    calculate_testim_metrics,
    calculate_device_metrics,
    calculate_epic_metrics,
    filter_epic_by_search
)
from modules.visualizations import (
    create_framework_pie_chart,
    create_testim_status_pie,
    create_testim_device_bar,
    create_device_totals_bar,
    create_device_status_stacked_bar,
    create_epic_top_bottom_bars,
    create_epic_complete_stacked_bar
)
from modules.exporter import (
    export_complete_data_to_excel,
    export_epic_data_to_excel,
    get_export_filename
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="QA Coverage Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        st.session_state.df_summary = None
        st.session_state.current_bu = None
        st.session_state.device_filter = ["Desktop", "Mobile", "Both"]
        st.session_state.country_filter = []
        st.session_state.priority_filter = []
        logger.info("Session state initialized")


def render_header():
    """Render the dashboard header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 QA Global Automation Coverage Dashboard")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        if validate_credentials():
            st.success("✅ Connected")
        else:
            st.error("❌ Not Connected")


def render_bu_selector():
    """Render business unit selector and update button"""
    col_select, col_button = st.columns([2.5, 1])

    with col_select:
        selected_bu = st.selectbox(
            "Select Business Unit",
            get_bu_names(),
            label_visibility="visible"
        )

    with col_button:
        st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)
        update_clicked = st.button(
            "🔄 Update Dashboard",
            type="primary",
            use_container_width=True
        )

    return selected_bu, update_clicked


def load_data(selected_bu: str):
    """Load and process data for selected business unit"""
    config = get_bu_config(selected_bu)

    with st.spinner(f"Fetching data for {selected_bu}..."):
        raw_df = fetch_data_recursive(config.project_id, config.suite_id)

    if raw_df.empty:
        st.error("❌ Failed to fetch data from TestRail")
        st.session_state.data_loaded = False
        logger.error(f"Failed to fetch data for {selected_bu}")
        return

    df_summary = process(raw_df, bu_name=selected_bu)

    if df_summary.empty:
        st.error("❌ No data after processing")
        st.session_state.data_loaded = False
        logger.error(f"Processing returned empty DataFrame for {selected_bu}")
        return

    st.session_state.df_summary = df_summary
    st.session_state.data_loaded = True
    st.session_state.current_bu = selected_bu
    logger.info(f"Data loaded successfully for {selected_bu}")


def get_unique_filter_values(df: pd.DataFrame, column: str, exclude_prefix: str = None) -> list:
    """
    Get unique filter values from a column

    Args:
        df: DataFrame to extract values from
        column: Column name
        exclude_prefix: Optional prefix to exclude (e.g., 'ID_')

    Returns:
        Sorted list of unique values
    """
    if column not in df.columns:
        return []

    all_values = set()
    for value_str in df[column].unique():
        if value_str == 'Unknown':
            continue
        if ', ' in str(value_str):
            for value in str(value_str).split(', '):
                if not exclude_prefix or not value.startswith(exclude_prefix):
                    all_values.add(value)
        else:
            if not exclude_prefix or not str(value_str).startswith(exclude_prefix):
                all_values.add(str(value_str))

    return sorted(list(all_values))


def render_filters(df_summary: pd.DataFrame):
    """Render filter controls"""
    col_filters_header, col_reset = st.columns([5, 1])

    with col_filters_header:
        st.subheader("🔍 Filters")

    with col_reset:
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.session_state.device_filter = ["Desktop", "Mobile", "Both"]
            st.session_state.country_filter = get_unique_filter_values(df_summary, 'Country', 'ID_')
            st.session_state.priority_filter = get_unique_filter_values(df_summary, 'Priority')
            st.rerun()

    col_filter1, col_filter2, col_filter3 = st.columns(3)

    with col_filter1:
        device_filter = st.multiselect(
            "Device Type",
            options=["Desktop", "Mobile", "Both"],
            default=st.session_state.device_filter,
            key="device_filter"
        )

    with col_filter2:
        country_options = get_unique_filter_values(df_summary, 'Country', 'ID_')
        if not st.session_state.country_filter:
            st.session_state.country_filter = country_options
        country_filter = st.multiselect(
            "Country",
            options=country_options,
            default=st.session_state.country_filter,
            key="country_filter"
        )

    with col_filter3:
        priority_options = get_unique_filter_values(df_summary, 'Priority')
        if not st.session_state.priority_filter:
            st.session_state.priority_filter = priority_options
        priority_filter = st.multiselect(
            "Priority",
            options=priority_options,
            default=st.session_state.priority_filter,
            key="priority_filter"
        )

    return device_filter, country_filter, priority_filter


def apply_filters(df: pd.DataFrame, device_filter: list, country_filter: list, priority_filter: list) -> pd.DataFrame:
    """Apply filters to the summary DataFrame"""
    df_filtered = df[df['Device'].isin(device_filter)]

    if country_filter and 'Country' in df.columns:
        def country_matches_filter(country_str, filter_list):
            if country_str == 'Unknown':
                return False
            if ', ' in country_str:
                return any(c in filter_list for c in country_str.split(', '))
            return country_str in filter_list

        df_filtered = df_filtered[df_filtered['Country'].apply(lambda x: country_matches_filter(x, country_filter))]

    if priority_filter and 'Priority' in df.columns:
        df_filtered = df_filtered[df_filtered['Priority'].isin(priority_filter)]

    return df_filtered


def render_overall_coverage(metrics: dict):
    """Render overall coverage summary section"""
    st.header("📊 Overall Coverage Summary")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.metric("Total Test Cases", f"{metrics['total']:,}")
        st.metric(
            "Effective Coverage",
            f"{metrics['coverage']:.1f}%",
            help="Total Automated / (Total - N/A)"
        )
        st.metric("Total Automated", f"{metrics['total_automated']:,}")
        st.metric("To Be Automated", f"{metrics['to_be_automated']:,}")
        st.metric("Not Automated", f"{metrics['not_automated']:,}")
        st.metric("Not Applicable", f"{metrics['not_applicable']:,}")

    with col2:
        st.markdown("### 🔧 Framework Breakdown")
        java_pct = (metrics['automated_java'] / metrics['effective_total'] * 100) if metrics['effective_total'] > 0 else 0
        testim_pct = (metrics['total_testim'] / metrics['effective_total'] * 100) if metrics['effective_total'] > 0 else 0

        st.metric(
            "Java Framework",
            f"{metrics['automated_java']:,}",
            delta=f"{java_pct:.1f}%"
        )
        st.metric(
            "Testim Framework",
            f"{metrics['total_testim']:,}",
            delta=f"{testim_pct:.1f}%"
        )

        st.markdown("##### Testim Details:")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.caption("Desktop Only")
            st.markdown(f"**{metrics['automated_testim_desktop']:,}**")
            st.caption("Mobile Only")
            st.markdown(f"**{metrics['automated_testim_mobile']:,}**")
        with col_t2:
            st.caption("Both")
            st.markdown(f"**{metrics['automated_testim_both']:,}**")

    with col3:
        fig_framework = create_framework_pie_chart(metrics)
        if fig_framework.data:
            st.plotly_chart(fig_framework, use_container_width=True)


def render_testim_section(testim_metrics: dict):
    """Render Testim framework breakdown section"""
    st.divider()
    st.subheader("🧪 Testim Framework Breakdown")

    col_testim1, col_testim2 = st.columns([2, 3])

    with col_testim1:
        st.markdown("#### 📊 Testim Status Overview")
        st.metric("Total Cases for Testim", f"{testim_metrics['testim_total']:,}")
        st.metric(
            "Testim Coverage",
            f"{testim_metrics['testim_coverage']:.1f}%",
            delta=f"{testim_metrics['total_testim']}/{testim_metrics['testim_total']}"
        )

        fig_testim_status = create_testim_status_pie(testim_metrics)
        if fig_testim_status.data:
            st.plotly_chart(fig_testim_status, use_container_width=True)

    with col_testim2:
        st.markdown("#### 📱 Device Coverage Details")

        col_t_desk, col_t_mob, col_t_both = st.columns(3)

        with col_t_desk:
            st.markdown("**🖥️ Desktop Only**")
            st.metric("Automated", f"{testim_metrics['desktop']:,}")
            st.caption(f"{testim_metrics['desktop_pct']:.1f}% of Testim")

        with col_t_mob:
            st.markdown("**📱 Mobile Only**")
            st.metric("Automated", f"{testim_metrics['mobile']:,}")
            st.caption(f"{testim_metrics['mobile_pct']:.1f}% of Testim")

        with col_t_both:
            st.markdown("**💻📱 Both**")
            st.metric("Automated", f"{testim_metrics['both']:,}")
            st.caption(f"{testim_metrics['both_pct']:.1f}% of Testim")

        st.markdown("---")

        fig_testim_device = create_testim_device_bar(testim_metrics)
        if fig_testim_device.data:
            st.plotly_chart(fig_testim_device, use_container_width=True)


def render_device_section(df_filtered: pd.DataFrame, device_metrics: dict):
    """Render device distribution section"""
    st.divider()
    st.subheader("📱 Distribution by Device")

    col_dev1, col_dev2 = st.columns(2)

    with col_dev1:
        fig_device = create_device_totals_bar(df_filtered)
        if fig_device.data:
            st.plotly_chart(fig_device, use_container_width=True)

    with col_dev2:
        fig_device_status = create_device_status_stacked_bar(df_filtered)
        if fig_device_status.data:
            st.plotly_chart(fig_device_status, use_container_width=True)

    st.markdown("#### 📊 Automation by Device")
    col_dev_stats1, col_dev_stats2, col_dev_stats3 = st.columns(3)

    with col_dev_stats1:
        desktop = device_metrics.get('Desktop', {})
        st.metric(
            "🖥️ Desktop Coverage",
            f"{desktop.get('coverage', 0):.1f}%",
            delta=f"{desktop.get('automated', 0)}/{desktop.get('total', 0)}",
            help=f"Automated: {desktop.get('automated', 0)}, Total: {desktop.get('total', 0)}"
        )

    with col_dev_stats2:
        mobile = device_metrics.get('Mobile', {})
        st.metric(
            "📱 Mobile Coverage",
            f"{mobile.get('coverage', 0):.1f}%",
            delta=f"{mobile.get('automated', 0)}/{mobile.get('total', 0)}",
            help=f"Automated: {mobile.get('automated', 0)}, Total: {mobile.get('total', 0)}"
        )

    with col_dev_stats3:
        both = device_metrics.get('Both', {})
        st.metric(
            "💻📱 Both Coverage",
            f"{both.get('coverage', 0):.1f}%",
            delta=f"{both.get('automated', 0)}/{both.get('total', 0)}",
            help=f"Automated: {both.get('automated', 0)}, Total: {both.get('total', 0)}"
        )


def render_epic_section(df_filtered: pd.DataFrame):
    """Render epic coverage section"""
    st.divider()
    st.subheader("🎯 Coverage by Epic")

    pivot, epic_stats = calculate_epic_metrics(df_filtered)

    if pivot.empty:
        st.warning("No epic data available")
        return

    # Search functionality
    epic_search = st.text_input(
        "🔍 Search Epic",
        placeholder="Type to filter epics...",
        key="epic_search"
    )

    pivot_filtered = filter_epic_by_search(pivot, epic_search)
    num_epics = len(pivot_filtered)
    st.caption(f"Showing {num_epics} epic(s)")

    # Top and bottom charts
    col_top, col_bottom = st.columns(2)

    fig_top, fig_bottom = create_epic_top_bottom_bars(pivot_filtered, top_n=10)

    with col_top:
        st.markdown("### 🏆 Top 10 - Best Coverage")
        if fig_top.data:
            st.plotly_chart(fig_top, use_container_width=True)

    with col_bottom:
        st.markdown("### ⚠️ Bottom 10 - Needs Attention")
        if fig_bottom.data:
            st.plotly_chart(fig_bottom, use_container_width=True)

    # Statistics
    col_stats1, col_stats2, col_stats3 = st.columns(3)

    with col_stats1:
        st.metric("📊 Average Coverage", f"{epic_stats['avg_coverage']:.1f}%")

    with col_stats2:
        st.metric(
            "✅ Epics ≥50% Coverage",
            f"{epic_stats['epics_above_50']}/{epic_stats['num_epics']}"
        )

    with col_stats3:
        st.metric(
            "🚨 Epics <30% Coverage",
            f"{epic_stats['epics_below_30']}/{epic_stats['num_epics']}"
        )

    # Complete breakdown
    with st.expander("📊 Complete Epic Breakdown (All Epics)", expanded=False):
        col_chart, col_table = st.columns([2, 1])

        with col_chart:
            fig_all = create_epic_complete_stacked_bar(pivot_filtered)
            if fig_all.data:
                st.plotly_chart(fig_all, use_container_width=True)

        with col_table:
            st.dataframe(
                pivot_filtered[['Automated', 'To Be Automated', 'Not Automated', 'TOTAL', 'COVERAGE %']],
                use_container_width=True,
                height=600
            )

    return pivot


def render_export_section(df_summary: pd.DataFrame, pivot: pd.DataFrame, overall_metrics: dict,
                          testim_metrics: dict, device_metrics: dict, bu_name: str):
    """Render export functionality section"""
    st.divider()
    st.subheader("📥 Export Data")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        if st.button("📊 Export Epic Coverage (Excel)", use_container_width=True):
            try:
                excel_data = export_epic_data_to_excel(pivot, overall_metrics, bu_name)
                filename = f"{get_export_filename(bu_name, 'epic')}.xlsx"
                st.download_button(
                    label="⬇️ Download Epic Coverage",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Epic export ready!")
            except Exception as e:
                st.error(f"Export failed: {e}")
                logger.error(f"Epic export error: {e}", exc_info=True)

    with col_exp2:
        if st.button("📈 Export Complete Dashboard (Excel)", use_container_width=True):
            try:
                excel_data = export_complete_data_to_excel(
                    df_summary, pivot, overall_metrics, testim_metrics, device_metrics, bu_name
                )
                filename = f"{get_export_filename(bu_name, 'complete')}.xlsx"
                st.download_button(
                    label="⬇️ Download Complete Data",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Complete export ready!")
            except Exception as e:
                st.error(f"Export failed: {e}")
                logger.error(f"Complete export error: {e}", exc_info=True)

    with col_exp3:
        st.caption("Export options provide detailed Excel reports with multiple sheets for analysis")


def main():
    """Main application function"""
    initialize_session_state()
    render_header()

    st.divider()

    selected_bu, update_clicked = render_bu_selector()

    # Load data if needed
    if update_clicked or (st.session_state.data_loaded and st.session_state.current_bu != selected_bu):
        load_data(selected_bu)

    # Render dashboard if data is loaded
    if st.session_state.data_loaded:
        df_summary = st.session_state.df_summary

        # Render filters
        device_filter, country_filter, priority_filter = render_filters(df_summary)

        # Apply filters
        df_filtered = apply_filters(df_summary, device_filter, country_filter, priority_filter)

        if df_filtered.empty:
            st.warning("⚠️ No data matches the selected filters")
        else:
            # Calculate all metrics
            overall_metrics = calculate_overall_metrics(df_filtered)
            testim_metrics = calculate_testim_metrics(df_filtered)
            device_metrics = calculate_device_metrics(df_filtered)

            # Render sections
            render_overall_coverage(overall_metrics)
            render_testim_section(testim_metrics)
            render_device_section(df_filtered, device_metrics)
            pivot = render_epic_section(df_filtered)

            # Export section
            if pivot is not None:
                render_export_section(
                    df_filtered, pivot, overall_metrics,
                    testim_metrics, device_metrics,
                    st.session_state.current_bu
                )

            st.success(f"✅ Dashboard updated successfully for {st.session_state.current_bu}")
    else:
        st.info("👆 Select the desired Business Unit and click 'Update Dashboard' to load the latest data")


if __name__ == "__main__":
    main()
