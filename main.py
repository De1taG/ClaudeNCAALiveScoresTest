"""NCAA Sports Tracker - Main GUI Application"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

from ncaa_api import NCAAAPIClient
from xml_generator import XMLGenerator
from config_manager import ConfigManager


class NCAATrackerApp(ctk.CTk):
    """Main application window for NCAA Sports Tracker"""

    def __init__(self):
        super().__init__()

        # Initialize components
        self.config = ConfigManager()
        self.api_client = NCAAAPIClient()
        self.xml_generator = XMLGenerator()

        # Application state
        self.selected_contests = []
        self.all_contests = []
        self.auto_update_thread = None
        self.auto_update_running = False
        self.last_xml_path = None

        # Setup UI
        self.title("NCAA Sports Tracker")
        self.geometry("1400x900")

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._create_widgets()
        self._load_initial_data()

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left sidebar for filters
        self._create_sidebar()

        # Main content area
        self._create_main_area()

        # Bottom control panel
        self._create_control_panel()

    def _create_sidebar(self):
        """Create left sidebar with filters"""
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar.grid_rowconfigure(12, weight=1)

        # Title
        title = ctk.CTkLabel(sidebar, text="NCAA Sports Tracker",
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sport selection
        ctk.CTkLabel(sidebar, text="Sport:", anchor="w").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.sport_var = ctk.StringVar(value="Women's Basketball")
        self.sport_menu = ctk.CTkOptionMenu(sidebar, values=list(self.api_client.SPORT_CODES.keys()),
                                           variable=self.sport_var, command=self._on_filter_change)
        self.sport_menu.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Division selection
        ctk.CTkLabel(sidebar, text="Division:", anchor="w").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.division_var = ctk.StringVar(value="Division I")
        self.division_menu = ctk.CTkOptionMenu(sidebar, values=list(self.api_client.DIVISIONS.keys()),
                                              variable=self.division_var, command=self._on_filter_change)
        self.division_menu.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        # Date selection
        ctk.CTkLabel(sidebar, text="Date:", anchor="w").grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%m/%d/%Y"))
        self.date_entry = ctk.CTkEntry(sidebar, textvariable=self.date_var, placeholder_text="MM/DD/YYYY")
        self.date_entry.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        # Quick date buttons
        date_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        date_frame.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        date_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(date_frame, text="Today", command=lambda: self._set_date(0), width=60).grid(row=0, column=0, padx=2)
        ctk.CTkButton(date_frame, text="Tomorrow", command=lambda: self._set_date(1), width=60).grid(row=0, column=1, padx=2)
        ctk.CTkButton(date_frame, text="+7", command=lambda: self._set_date(7), width=60).grid(row=0, column=2, padx=2)

        # Week selection (optional)
        ctk.CTkLabel(sidebar, text="Week (optional):", anchor="w").grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
        self.week_var = ctk.StringVar(value="")
        self.week_entry = ctk.CTkEntry(sidebar, textvariable=self.week_var, placeholder_text="Leave blank for date")
        self.week_entry.grid(row=9, column=0, padx=20, pady=5, sticky="ew")

        # Filter options
        self.top25_var = ctk.BooleanVar(value=False)
        self.top25_check = ctk.CTkCheckBox(sidebar, text="Top 25 Only", variable=self.top25_var,
                                          command=self._apply_filters)
        self.top25_check.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        # Conference filter
        ctk.CTkLabel(sidebar, text="Conference Filter:", anchor="w").grid(row=11, column=0, padx=20, pady=(10, 0), sticky="w")
        self.conference_var = ctk.StringVar(value="All")
        self.conference_entry = ctk.CTkEntry(sidebar, textvariable=self.conference_var, placeholder_text="All conferences")
        self.conference_entry.grid(row=12, column=0, padx=20, pady=5, sticky="ew")

        # Fetch button
        self.fetch_btn = ctk.CTkButton(sidebar, text="Fetch Events", command=self._fetch_events,
                                      font=ctk.CTkFont(size=14, weight="bold"), height=40)
        self.fetch_btn.grid(row=13, column=0, padx=20, pady=20, sticky="ew")

        # Status label
        self.status_label = ctk.CTkLabel(sidebar, text="Ready", font=ctk.CTkFont(size=11))
        self.status_label.grid(row=14, column=0, padx=20, pady=(0, 10))

    def _create_main_area(self):
        """Create main content area"""
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Top section - Available events
        available_label = ctk.CTkLabel(main_frame, text="Available Events",
                                      font=ctk.CTkFont(size=16, weight="bold"))
        available_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Events list with scrollbar
        events_container = ctk.CTkFrame(main_frame)
        events_container.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        events_container.grid_columnconfigure(0, weight=1)
        events_container.grid_rowconfigure(0, weight=1)

        self.events_text = ctk.CTkTextbox(events_container, font=ctk.CTkFont(size=12))
        self.events_text.grid(row=0, column=0, sticky="nsew")

        # Selected events section
        selected_label = ctk.CTkLabel(main_frame, text="Selected Events (Click to Remove)",
                                     font=ctk.CTkFont(size=16, weight="bold"))
        selected_label.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="w")

        selected_container = ctk.CTkFrame(main_frame)
        selected_container.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        selected_container.grid_columnconfigure(0, weight=1)
        selected_container.grid_rowconfigure(0, weight=1)

        self.selected_text = ctk.CTkTextbox(selected_container, height=150, font=ctk.CTkFont(size=11))
        self.selected_text.grid(row=0, column=0, sticky="nsew")
        self.selected_text.configure(state="disabled")

        # Configure row weights for proper sizing
        main_frame.grid_rowconfigure(1, weight=3)
        main_frame.grid_rowconfigure(3, weight=1)

        # Bind click events
        self.events_text.bind("<Button-1>", self._on_event_click)
        self.selected_text.bind("<Button-1>", self._on_selected_click)

    def _create_control_panel(self):
        """Create bottom control panel"""
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        control_frame.grid_columnconfigure(1, weight=1)

        # Auto-update controls
        auto_frame = ctk.CTkFrame(control_frame)
        auto_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(auto_frame, text="Auto-update interval (sec):").grid(row=0, column=0, padx=5)
        self.interval_var = ctk.StringVar(value=str(self.config.get('update_interval', 60)))
        self.interval_entry = ctk.CTkEntry(auto_frame, textvariable=self.interval_var, width=60)
        self.interval_entry.grid(row=0, column=1, padx=5)

        self.start_btn = ctk.CTkButton(auto_frame, text="▶ Start Auto-Update", command=self._start_auto_update,
                                      fg_color="green", hover_color="darkgreen", width=140)
        self.start_btn.grid(row=0, column=2, padx=5)

        self.stop_btn = ctk.CTkButton(auto_frame, text="⏹ Stop", command=self._stop_auto_update,
                                     fg_color="red", hover_color="darkred", width=100, state="disabled")
        self.stop_btn.grid(row=0, column=3, padx=5)

        # Action buttons
        action_frame = ctk.CTkFrame(control_frame)
        action_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.clear_btn = ctk.CTkButton(action_frame, text="Clear Selected", command=self._clear_selected, width=120)
        self.clear_btn.grid(row=0, column=0, padx=5)

        self.preview_btn = ctk.CTkButton(action_frame, text="Preview XML", command=self._preview_xml,
                                        fg_color="purple", hover_color="darkviolet", width=120)
        self.preview_btn.grid(row=0, column=1, padx=5)

        self.save_btn = ctk.CTkButton(action_frame, text="💾 Save XML", command=self._save_xml,
                                     font=ctk.CTkFont(size=14, weight="bold"), width=140, height=35)
        self.save_btn.grid(row=0, column=2, padx=5)

    def _set_date(self, days_offset: int):
        """Set date with offset from today"""
        new_date = datetime.now() + timedelta(days=days_offset)
        self.date_var.set(new_date.strftime("%m/%d/%Y"))

    def _on_filter_change(self, *args):
        """Handle filter changes"""
        pass

    def _load_initial_data(self):
        """Load initial data on startup"""
        self.after(500, self._fetch_events)

    def _fetch_events(self):
        """Fetch events from NCAA API"""
        self.status_label.configure(text="Fetching...")
        self.fetch_btn.configure(state="disabled")

        def fetch_thread():
            try:
                sport_code = self.api_client.SPORT_CODES[self.sport_var.get()]
                division = self.api_client.DIVISIONS[self.division_var.get()]
                date = self.date_var.get()
                week = self.week_var.get() if self.week_var.get() else None

                # Fetch data
                response = self.api_client.fetch_contests(
                    sport_code=sport_code,
                    division=division,
                    season_year=2025,
                    contest_date=date,
                    week=int(week) if week else None
                )

                # Parse contests
                self.all_contests = self.api_client.parse_contests(response)

                # Update UI on main thread
                self.after(0, self._display_events)
                self.after(0, lambda: self.status_label.configure(text=f"Found {len(self.all_contests)} events"))
                self.after(0, lambda: self.fetch_btn.configure(state="normal"))

            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}"))
                self.after(0, lambda: self.fetch_btn.configure(state="normal"))

        threading.Thread(target=fetch_thread, daemon=True).start()

    def _display_events(self):
        """Display events in the text widget"""
        self.events_text.delete("1.0", "end")

        # Apply filters
        filtered_contests = self._apply_filters()

        if not filtered_contests:
            self.events_text.insert("1.0", "No events found matching your criteria.\n\nTry adjusting filters or fetching a different date.")
            return

        for i, contest in enumerate(filtered_contests):
            # Format event display
            home_team = contest.get('home_team', {})
            away_team = contest.get('away_team', {})

            # Build display string
            home_name = home_team.get('name', 'TBD')
            away_name = away_team.get('name', 'TBD')
            home_rank = f" (#{home_team.get('rank')})" if home_team.get('rank') else ""
            away_rank = f" (#{away_team.get('rank')})" if away_team.get('rank') else ""

            display_text = f"[{i}] {away_name}{away_rank} @ {home_name}{home_rank}\n"
            display_text += f"    📅 {contest.get('date', 'TBD')} {contest.get('time', '')}\n"

            if home_team.get('conference'):
                display_text += f"    🏆 {home_team.get('conference')}\n"

            if contest.get('venue'):
                display_text += f"    📍 {contest.get('venue')}\n"

            if contest.get('broadcast'):
                display_text += f"    📺 {contest.get('broadcast')}\n"

            display_text += "\n"

            self.events_text.insert("end", display_text)

    def _apply_filters(self) -> List[Dict]:
        """Apply current filters to contests"""
        filtered = self.all_contests.copy()

        # Top 25 filter
        if self.top25_var.get():
            filtered = [c for c in filtered if self.api_client.is_top_25(c)]

        # Conference filter
        conf_filter = self.conference_var.get().strip()
        if conf_filter and conf_filter.lower() != "all":
            filtered = [c for c in filtered if
                       conf_filter.lower() in c.get('home_team', {}).get('conference', '').lower() or
                       conf_filter.lower() in c.get('away_team', {}).get('conference', '').lower()]

        return filtered

    def _on_event_click(self, event):
        """Handle click on event in available events list"""
        try:
            # Get clicked line
            index = self.events_text.index(f"@{event.x},{event.y}")
            line_text = self.events_text.get(f"{index} linestart", f"{index} lineend")

            # Extract event index
            if line_text.startswith("["):
                event_idx = int(line_text.split("]")[0][1:])
                filtered = self._apply_filters()

                if 0 <= event_idx < len(filtered):
                    contest = filtered[event_idx]
                    if contest not in self.selected_contests:
                        self.selected_contests.append(contest)
                        self._update_selected_display()

        except Exception as e:
            print(f"Error selecting event: {e}")

    def _on_selected_click(self, event):
        """Handle click on selected event (to remove)"""
        try:
            index = self.selected_text.index(f"@{event.x},{event.y}")
            line_text = self.selected_text.get(f"{index} linestart", f"{index} lineend")

            if line_text.startswith("["):
                event_idx = int(line_text.split("]")[0][1:])

                if 0 <= event_idx < len(self.selected_contests):
                    self.selected_contests.pop(event_idx)
                    self._update_selected_display()

        except Exception as e:
            print(f"Error removing event: {e}")

    def _update_selected_display(self):
        """Update selected events display"""
        self.selected_text.configure(state="normal")
        self.selected_text.delete("1.0", "end")

        if not self.selected_contests:
            self.selected_text.insert("1.0", "No events selected. Click on events above to add them.")
        else:
            for i, contest in enumerate(self.selected_contests):
                home_team = contest.get('home_team', {})
                away_team = contest.get('away_team', {})

                display = f"[{i}] {away_team.get('name', 'TBD')} @ {home_team.get('name', 'TBD')} - {contest.get('date', 'TBD')}\n"
                self.selected_text.insert("end", display)

        self.selected_text.configure(state="disabled")

    def _clear_selected(self):
        """Clear all selected events"""
        self.selected_contests.clear()
        self._update_selected_display()

    def _preview_xml(self):
        """Preview generated XML"""
        if not self.selected_contests:
            messagebox.showwarning("No Events", "Please select at least one event first.")
            return

        # Generate XML
        metadata = {
            'Sport': self.sport_var.get(),
            'Division': self.division_var.get(),
            'Date': self.date_var.get(),
            'TotalEvents': len(self.selected_contests)
        }

        xml_string = self.xml_generator.generate_xml(self.selected_contests, metadata)

        # Show preview window
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("XML Preview")
        preview_window.geometry("800x600")

        text_widget = ctk.CTkTextbox(preview_window, font=ctk.CTkFont(family="Courier", size=11))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", xml_string)

        close_btn = ctk.CTkButton(preview_window, text="Close", command=preview_window.destroy)
        close_btn.pack(pady=10)

    def _save_xml(self):
        """Save XML to file"""
        if not self.selected_contests:
            messagebox.showwarning("No Events", "Please select at least one event first.")
            return

        # Get save location
        initial_dir = self.config.get('last_save_directory', os.path.expanduser('~'))
        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            title="Save NCAA Events XML"
        )

        if file_path:
            # Generate and save XML
            metadata = {
                'Sport': self.sport_var.get(),
                'Division': self.division_var.get(),
                'Date': self.date_var.get(),
                'TotalEvents': len(self.selected_contests)
            }

            xml_string = self.xml_generator.generate_xml(self.selected_contests, metadata)

            if self.xml_generator.save_to_file(xml_string, file_path):
                # Save directory for next time
                self.config.set('last_save_directory', os.path.dirname(file_path))
                self.last_xml_path = file_path
                messagebox.showinfo("Success", f"XML saved successfully to:\n{file_path}")
            else:
                messagebox.showerror("Error", "Failed to save XML file.")

    def _start_auto_update(self):
        """Start auto-update thread"""
        try:
            interval = int(self.interval_var.get())
            if interval < 5:
                messagebox.showwarning("Invalid Interval", "Interval must be at least 5 seconds.")
                return

            if not self.selected_contests or not self.last_xml_path:
                messagebox.showwarning("Setup Required",
                                      "Please select events and save XML at least once before starting auto-update.")
                return

            self.auto_update_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="Auto-update running...")

            def auto_update_loop():
                while self.auto_update_running:
                    time.sleep(interval)
                    if self.auto_update_running:
                        self._update_xml()

            self.auto_update_thread = threading.Thread(target=auto_update_loop, daemon=True)
            self.auto_update_thread.start()

        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid number for the interval.")

    def _stop_auto_update(self):
        """Stop auto-update thread"""
        self.auto_update_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Auto-update stopped")

    def _update_xml(self):
        """Update XML file (called by auto-update)"""
        if not self.last_xml_path:
            return

        try:
            # Re-fetch current data
            sport_code = self.api_client.SPORT_CODES[self.sport_var.get()]
            division = self.api_client.DIVISIONS[self.division_var.get()]
            date = self.date_var.get()
            week = self.week_var.get() if self.week_var.get() else None

            response = self.api_client.fetch_contests(
                sport_code=sport_code,
                division=division,
                season_year=2025,
                contest_date=date,
                week=int(week) if week else None
            )

            updated_contests = self.api_client.parse_contests(response)

            # Update selected contests with fresh data
            updated_selected = []
            for selected in self.selected_contests:
                # Find matching contest in updated data
                matching = next((c for c in updated_contests if c.get('id') == selected.get('id')), None)
                if matching:
                    updated_selected.append(matching)
                else:
                    updated_selected.append(selected)

            # Generate and save updated XML
            metadata = {
                'Sport': self.sport_var.get(),
                'Division': self.division_var.get(),
                'Date': self.date_var.get(),
                'TotalEvents': len(updated_selected),
                'LastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            xml_string = self.xml_generator.generate_xml(updated_selected, metadata)
            self.xml_generator.save_to_file(xml_string, self.last_xml_path)

            self.after(0, lambda: self.status_label.configure(
                text=f"Auto-updated at {datetime.now().strftime('%H:%M:%S')}"))

        except Exception as e:
            print(f"Auto-update error: {e}")

    def on_closing(self):
        """Handle window close"""
        self._stop_auto_update()
        self.destroy()


def main():
    """Main entry point"""
    app = NCAATrackerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
