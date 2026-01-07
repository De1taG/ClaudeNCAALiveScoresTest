"""NCAA Sports Tracker - Web Version (Streamlit)"""
import streamlit as st
from datetime import datetime, timedelta
import time
import threading
from ncaa_api import NCAAAPIClient
from xml_generator import XMLGenerator
from config_manager import ConfigManager
import os

# Page configuration
st.set_page_config(
    page_title="NCAA Sports Tracker",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .event-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #0066cc;
    }
    .selected-event {
        background-color: #e6f3ff;
        border-left: 5px solid #00cc66;
    }
    .stats-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_client' not in st.session_state:
    st.session_state.api_client = NCAAAPIClient()
    st.session_state.xml_generator = XMLGenerator()
    st.session_state.config = ConfigManager()
    st.session_state.all_contests = []
    st.session_state.selected_contests = []
    st.session_state.auto_update_running = False
    st.session_state.last_xml = None
    st.session_state.last_fetch_time = None

def fetch_events(sport_code, division, date, week=None):
    """Fetch events from NCAA API"""
    with st.spinner('Fetching events from NCAA.com...'):
        response = st.session_state.api_client.fetch_contests(
            sport_code=sport_code,
            division=division,
            season_year=2025,
            contest_date=date,
            week=int(week) if week else None
        )
        contests = st.session_state.api_client.parse_contests(response)
        st.session_state.all_contests = contests
        st.session_state.last_fetch_time = datetime.now()
        return contests

def apply_filters(contests, top25_only, conference_filter):
    """Apply filters to contests"""
    filtered = contests.copy()

    if top25_only:
        filtered = [c for c in filtered if st.session_state.api_client.is_top_25(c)]

    if conference_filter and conference_filter.lower() != "all":
        filtered = [c for c in filtered if
                   conference_filter.lower() in c.get('home_team', {}).get('conference', '').lower() or
                   conference_filter.lower() in c.get('away_team', {}).get('conference', '').lower()]

    return filtered

def format_event_display(contest, index):
    """Format event for display"""
    home_team = contest.get('home_team', {})
    away_team = contest.get('away_team', {})

    home_name = home_team.get('name', 'TBD')
    away_name = away_team.get('name', 'TBD')
    home_rank = f" (#{home_team.get('rank')})" if home_team.get('rank') else ""
    away_rank = f" (#{away_team.get('rank')})" if away_team.get('rank') else ""

    display = f"**{away_name}{away_rank}** @ **{home_name}{home_rank}**\n\n"
    display += f"📅 {contest.get('date', 'TBD')} {contest.get('time', '')}\n\n"

    if home_team.get('conference'):
        display += f"🏆 {home_team.get('conference')}\n\n"

    if contest.get('venue'):
        display += f"📍 {contest.get('venue')}\n\n"

    if contest.get('broadcast'):
        display += f"📺 {contest.get('broadcast')}\n\n"

    if home_team.get('record') or away_team.get('record'):
        display += f"📊 {away_team.get('record', 'N/A')} vs {home_team.get('record', 'N/A')}"

    return display

# Main app
st.markdown('<h1 class="main-header">🏀 NCAA Sports Tracker</h1>', unsafe_allow_html=True)

# Sidebar - Filters and Controls
with st.sidebar:
    st.header("⚙️ Filters & Settings")

    # Sport selection
    sport_name = st.selectbox(
        "Sport",
        list(st.session_state.api_client.SPORT_CODES.keys()),
        index=0
    )
    sport_code = st.session_state.api_client.SPORT_CODES[sport_name]

    # Division selection
    division_name = st.selectbox(
        "Division",
        list(st.session_state.api_client.DIVISIONS.keys()),
        index=0
    )
    division = st.session_state.api_client.DIVISIONS[division_name]

    st.divider()

    # Date selection
    st.subheader("📅 Date Selection")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Today", use_container_width=True):
            st.session_state.selected_date = datetime.now()
    with col2:
        if st.button("Tomorrow", use_container_width=True):
            st.session_state.selected_date = datetime.now() + timedelta(days=1)
    with col3:
        if st.button("+7 Days", use_container_width=True):
            st.session_state.selected_date = datetime.now() + timedelta(days=7)

    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now()

    date_input = st.date_input(
        "Select Date",
        value=st.session_state.selected_date,
        key="date_picker"
    )
    date_str = date_input.strftime("%m/%d/%Y")

    # Week selection (optional)
    week_input = st.text_input("Week (optional)", "", placeholder="Leave blank for date")

    st.divider()

    # Filters
    st.subheader("🔍 Filters")

    top25_only = st.checkbox("Top 25 Only", value=False)
    conference_filter = st.text_input("Conference", "", placeholder="All conferences")

    st.divider()

    # Fetch button
    if st.button("🔄 Fetch Events", type="primary", use_container_width=True):
        fetch_events(sport_code, division, date_str, week_input)

    # Auto-refresh
    st.divider()
    st.subheader("🔄 Auto-Refresh")
    auto_refresh = st.checkbox("Enable Auto-Refresh")
    if auto_refresh:
        refresh_interval = st.slider("Interval (seconds)", 10, 300, 60)
        if st.session_state.last_fetch_time:
            time_since = (datetime.now() - st.session_state.last_fetch_time).total_seconds()
            if time_since >= refresh_interval:
                fetch_events(sport_code, division, date_str, week_input)
                st.rerun()
        st.info(f"Page will refresh every {refresh_interval} seconds")
        time.sleep(1)
        st.rerun()

    # Status
    if st.session_state.last_fetch_time:
        st.caption(f"Last fetch: {st.session_state.last_fetch_time.strftime('%H:%M:%S')}")

# Main content area
col_main1, col_main2 = st.columns([2, 1])

with col_main1:
    st.header("📋 Available Events")

    # Statistics
    if st.session_state.all_contests:
        filtered_contests = apply_filters(
            st.session_state.all_contests,
            top25_only,
            conference_filter
        )

        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Total Events", len(st.session_state.all_contests))
        with stat_col2:
            st.metric("Filtered Events", len(filtered_contests))
        with stat_col3:
            st.metric("Selected", len(st.session_state.selected_contests))

        st.divider()

        # Display events
        if filtered_contests:
            st.info("💡 Click 'Add' to select events for XML export")

            for i, contest in enumerate(filtered_contests):
                is_selected = contest in st.session_state.selected_contests

                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(format_event_display(contest, i))

                    with col2:
                        if is_selected:
                            if st.button("✓ Added", key=f"remove_{i}", use_container_width=True):
                                st.session_state.selected_contests.remove(contest)
                                st.rerun()
                        else:
                            if st.button("➕ Add", key=f"add_{i}", type="primary", use_container_width=True):
                                st.session_state.selected_contests.append(contest)
                                st.rerun()

                    st.divider()
        else:
            st.warning("No events match your filters. Try adjusting the filters or fetch a different date.")
    else:
        st.info("👈 Select filters and click 'Fetch Events' to get started!")
        st.markdown("""
        ### How to use:
        1. **Select Sport & Division** in the sidebar
        2. **Choose a Date** (or use quick buttons)
        3. **Click 'Fetch Events'** to retrieve data
        4. **Apply Filters** (optional: Top 25, Conference)
        5. **Click 'Add'** on events to select them
        6. **Generate & Download XML** from the right panel
        """)

with col_main2:
    st.header("✅ Selected Events")

    if st.session_state.selected_contests:
        st.success(f"{len(st.session_state.selected_contests)} events selected")

        # Clear all button
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.selected_contests = []
            st.rerun()

        st.divider()

        # Display selected events
        for i, contest in enumerate(st.session_state.selected_contests):
            home_name = contest.get('home_team', {}).get('name', 'TBD')
            away_name = contest.get('away_team', {}).get('name', 'TBD')

            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"**{i+1}.** {away_name} @ {home_name}")
                st.caption(f"{contest.get('date', 'TBD')}")
            with col_b:
                if st.button("❌", key=f"del_{i}", help="Remove"):
                    st.session_state.selected_contests.pop(i)
                    st.rerun()

        st.divider()

        # XML Generation
        st.subheader("📄 Generate XML")

        if st.button("👁️ Preview XML", use_container_width=True):
            metadata = {
                'Sport': sport_name,
                'Division': division_name,
                'Date': date_str,
                'TotalEvents': len(st.session_state.selected_contests)
            }
            xml_string = st.session_state.xml_generator.generate_xml(
                st.session_state.selected_contests,
                metadata
            )
            st.session_state.last_xml = xml_string
            st.code(xml_string, language='xml')

        if st.button("💾 Download XML", type="primary", use_container_width=True):
            metadata = {
                'Sport': sport_name,
                'Division': division_name,
                'Date': date_str,
                'TotalEvents': len(st.session_state.selected_contests),
                'GeneratedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            xml_string = st.session_state.xml_generator.generate_xml(
                st.session_state.selected_contests,
                metadata
            )

            # Download button
            filename = f"ncaa_events_{sport_code}_{date_str.replace('/', '_')}.xml"
            st.download_button(
                label="⬇️ Download XML File",
                data=xml_string,
                file_name=filename,
                mime="application/xml",
                use_container_width=True
            )
            st.success(f"✓ XML ready! Click above to download as '{filename}'")

        # Auto-update XML feature
        st.divider()
        st.subheader("🔄 Auto-Update XML")
        st.info("Enable Auto-Refresh in the sidebar to keep your data current")

    else:
        st.info("No events selected yet.\n\nAdd events from the left panel to generate XML.")

# Footer
st.divider()
st.caption("NCAA Sports Tracker • Data from NCAA.com • Built with Streamlit")
