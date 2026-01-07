"""NCAA Sports Tracker - Main GUI Application (Standard Tkinter Version)"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

from ncaa_api import NCAAAPIClient
from xml_generator import XMLGenerator
from config_manager import ConfigManager


class NCAATrackerApp(tk.Tk):
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

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Modern color scheme
        self.bg_color = '#1a1a1a'
        self.fg_color = '#ffffff'
        self.accent_color = '#0066cc'
        self.secondary_bg = '#2d2d2d'

        self.configure(bg=self.bg_color)

        # Configure ttk styles
        self._configure_styles()

        self._create_widgets()
        self._load_initial_data()

    def _configure_styles(self):
        """Configure ttk styles for modern look"""
        # Frame styles
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Sidebar.TFrame', background=self.secondary_bg)
        self.style.configure('Control.TFrame', background=self.secondary_bg)

        # Label styles
        self.style.configure('Main.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Arial', 10))
        self.style.configure('Sidebar.TLabel', background=self.secondary_bg, foreground=self.fg_color, font=('Arial', 10))
        self.style.configure('Title.TLabel', background=self.secondary_bg, foreground=self.fg_color, font=('Arial', 18, 'bold'))
        self.style.configure('Heading.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Arial', 14, 'bold'))

        # Button styles
        self.style.configure('Action.TButton', font=('Arial', 11, 'bold'), padding=10)
        self.style.configure('Fetch.TButton', font=('Arial', 12, 'bold'), padding=15)

        # Entry and Combobox
        self.style.configure('TEntry', fieldbackground='white', font=('Arial', 10))
        self.style.configure('TCombobox', fieldbackground='white', font=('Arial', 10))

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
        sidebar = ttk.Frame(self, style='Sidebar.TFrame', width=280)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)

        # Title
        title = ttk.Label(sidebar, text="NCAA Sports Tracker", style='Title.TLabel')
        title.pack(padx=20, pady=(20, 30))

        # Sport selection
        ttk.Label(sidebar, text="Sport:", style='Sidebar.TLabel').pack(anchor='w', padx=20, pady=(10, 5))
        self.sport_var = tk.StringVar(value="Women's Basketball")
        self.sport_menu = ttk.Combobox(sidebar, values=list(self.api_client.SPORT_CODES.keys()),
                                      textvariable=self.sport_var, state='readonly', width=30)
        self.sport_menu.pack(padx=20, pady=5)

        # Division selection
        ttk.Label(sidebar, text="Division:", style='Sidebar.TLabel').pack(anchor='w', padx=20, pady=(10, 5))
        self.division_var = tk.StringVar(value="Division I")
        self.division_menu = ttk.Combobox(sidebar, values=list(self.api_client.DIVISIONS.keys()),
                                         textvariable=self.division_var, state='readonly', width=30)
        self.division_menu.pack(padx=20, pady=5)

        # Date selection
        ttk.Label(sidebar, text="Date:", style='Sidebar.TLabel').pack(anchor='w', padx=20, pady=(10, 5))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%m/%d/%Y"))
        self.date_entry = ttk.Entry(sidebar, textvariable=self.date_var, width=32)
        self.date_entry.pack(padx=20, pady=5)

        # Quick date buttons
        date_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        date_frame.pack(padx=20, pady=5)

        ttk.Button(date_frame, text="Today", command=lambda: self._set_date(0), width=8).pack(side='left', padx=2)
        ttk.Button(date_frame, text="Tomorrow", command=lambda: self._set_date(1), width=10).pack(side='left', padx=2)
        ttk.Button(date_frame, text="+7 Days", command=lambda: self._set_date(7), width=8).pack(side='left', padx=2)

        # Week selection
        ttk.Label(sidebar, text="Week (optional):", style='Sidebar.TLabel').pack(anchor='w', padx=20, pady=(10, 5))
        self.week_var = tk.StringVar(value="")
        self.week_entry = ttk.Entry(sidebar, textvariable=self.week_var, width=32)
        self.week_entry.pack(padx=20, pady=5)

        # Filter options
        filter_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        filter_frame.pack(padx=20, pady=10, anchor='w')

        self.top25_var = tk.BooleanVar(value=False)
        self.top25_check = ttk.Checkbutton(filter_frame, text="Top 25 Only", variable=self.top25_var,
                                          command=self._apply_filters_and_display)
        self.top25_check.pack(anchor='w')

        # Conference filter
        ttk.Label(sidebar, text="Conference Filter:", style='Sidebar.TLabel').pack(anchor='w', padx=20, pady=(10, 5))
        self.conference_var = tk.StringVar(value="All")
        self.conference_entry = ttk.Entry(sidebar, textvariable=self.conference_var, width=32)
        self.conference_entry.pack(padx=20, pady=5)

        ttk.Button(sidebar, text="Apply Filters", command=self._apply_filters_and_display).pack(padx=20, pady=5, fill='x')

        # Fetch button
        self.fetch_btn = ttk.Button(sidebar, text="🔄 Fetch Events", command=self._fetch_events,
                                   style='Fetch.TButton')
        self.fetch_btn.pack(padx=20, pady=20, fill='x')

        # Status label
        self.status_label = ttk.Label(sidebar, text="Ready", style='Sidebar.TLabel', font=('Arial', 9))
        self.status_label.pack(padx=20, pady=(0, 10))

    def _create_main_area(self):
        """Create main content area"""
        main_frame = ttk.Frame(self, style='Main.TFrame')
        main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=3)
        main_frame.grid_rowconfigure(3, weight=1)

        # Available events section
        available_label = ttk.Label(main_frame, text="Available Events (Click to Select)",
                                   style='Heading.TLabel')
        available_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Events list with scrollbar
        events_frame = ttk.Frame(main_frame, style='Main.TFrame')
        events_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        events_frame.grid_columnconfigure(0, weight=1)
        events_frame.grid_rowconfigure(0, weight=1)

        self.events_text = scrolledtext.ScrolledText(events_frame, font=('Consolas', 10),
                                                     bg='white', fg='black', wrap=tk.WORD)
        self.events_text.grid(row=0, column=0, sticky="nsew")

        # Selected events section
        selected_label = ttk.Label(main_frame, text="Selected Events (Click to Remove)",
                                  style='Heading.TLabel')
        selected_label.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="w")

        selected_frame = ttk.Frame(main_frame, style='Main.TFrame')
        selected_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        selected_frame.grid_columnconfigure(0, weight=1)
        selected_frame.grid_rowconfigure(0, weight=1)

        self.selected_text = scrolledtext.ScrolledText(selected_frame, font=('Consolas', 9),
                                                       bg='#f0f0f0', fg='black', wrap=tk.WORD)
        self.selected_text.grid(row=0, column=0, sticky="nsew")

        # Bind click events
        self.events_text.bind("<Button-1>", self._on_event_click)
        self.selected_text.bind("<Button-1>", self._on_selected_click)

    def _create_control_panel(self):
        """Create bottom control panel"""
        control_frame = ttk.Frame(self, style='Control.TFrame')
        control_frame.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Auto-update controls
        auto_frame = ttk.Frame(control_frame, style='Control.TFrame')
        auto_frame.pack(side='left', padx=10, pady=10)

        ttk.Label(auto_frame, text="Auto-update interval (sec):", style='Sidebar.TLabel').pack(side='left', padx=5)
        self.interval_var = tk.StringVar(value=str(self.config.get('update_interval', 60)))
        self.interval_entry = ttk.Entry(auto_frame, textvariable=self.interval_var, width=8)
        self.interval_entry.pack(side='left', padx=5)

        self.start_btn = tk.Button(auto_frame, text="▶ Start Auto-Update", command=self._start_auto_update,
                                   bg='green', fg='white', font=('Arial', 10, 'bold'),
                                   padx=10, pady=5, cursor='hand2')
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = tk.Button(auto_frame, text="⏹ Stop", command=self._stop_auto_update,
                                  bg='red', fg='white', font=('Arial', 10, 'bold'),
                                  padx=10, pady=5, state='disabled', cursor='hand2')
        self.stop_btn.pack(side='left', padx=5)

        # Action buttons
        action_frame = ttk.Frame(control_frame, style='Control.TFrame')
        action_frame.pack(side='right', padx=10, pady=10)

        ttk.Button(action_frame, text="Clear Selected", command=self._clear_selected,
                  style='Action.TButton').pack(side='left', padx=5)

        tk.Button(action_frame, text="Preview XML", command=self._preview_xml,
                 bg='purple', fg='white', font=('Arial', 10, 'bold'),
                 padx=10, pady=5, cursor='hand2').pack(side='left', padx=5)

        tk.Button(action_frame, text="💾 Save XML", command=self._save_xml,
                 bg=self.accent_color, fg='white', font=('Arial', 12, 'bold'),
                 padx=15, pady=8, cursor='hand2').pack(side='left', padx=5)

    def _set_date(self, days_offset: int):
        """Set date with offset from today"""
        new_date = datetime.now() + timedelta(days=days_offset)
        self.date_var.set(new_date.strftime("%m/%d/%Y"))

    def _load_initial_data(self):
        """Load initial data on startup"""
        self.after(500, self._fetch_events)

    def _fetch_events(self):
        """Fetch events from NCAA API"""
        self.status_label.config(text="Fetching...")
        self.fetch_btn.config(state='disabled')

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
                self.after(0, lambda: self.status_label.config(text=f"Found {len(self.all_contests)} events"))
                self.after(0, lambda: self.fetch_btn.config(state='normal'))

            except Exception as e:
                self.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))
                self.after(0, lambda: self.fetch_btn.config(state='normal'))

        threading.Thread(target=fetch_thread, daemon=True).start()

    def _apply_filters_and_display(self):
        """Apply filters and update display"""
        self._display_events()

    def _display_events(self):
        """Display events in the text widget"""
        self.events_text.delete("1.0", "end")

        # Apply filters
        filtered_contests = self._apply_filters()

        if not filtered_contests:
            self.events_text.insert("1.0", "No events found matching your criteria.\n\n" +
                                   "Try adjusting filters or fetching a different date.")
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
            display_text += f"    Date: {contest.get('date', 'TBD')} {contest.get('time', '')}\n"

            if home_team.get('conference'):
                display_text += f"    Conference: {home_team.get('conference')}\n"

            if contest.get('venue'):
                display_text += f"    Venue: {contest.get('venue')}\n"

            if contest.get('broadcast'):
                display_text += f"    TV: {contest.get('broadcast')}\n"

            if home_team.get('record'):
                display_text += f"    Records: {away_team.get('record', 'N/A')} vs {home_team.get('record', 'N/A')}\n"

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
                        self.status_label.config(text=f"Selected {len(self.selected_contests)} events")

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
                    self.status_label.config(text=f"Selected {len(self.selected_contests)} events")

        except Exception as e:
            print(f"Error removing event: {e}")

    def _update_selected_display(self):
        """Update selected events display"""
        self.selected_text.delete("1.0", "end")

        if not self.selected_contests:
            self.selected_text.insert("1.0", "No events selected. Click on events above to add them.")
        else:
            for i, contest in enumerate(self.selected_contests):
                home_team = contest.get('home_team', {})
                away_team = contest.get('away_team', {})

                display = (f"[{i}] {away_team.get('name', 'TBD')} @ {home_team.get('name', 'TBD')} - "
                          f"{contest.get('date', 'TBD')}\n")
                self.selected_text.insert("end", display)

    def _clear_selected(self):
        """Clear all selected events"""
        self.selected_contests.clear()
        self._update_selected_display()
        self.status_label.config(text="Cleared selected events")

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
        preview_window = tk.Toplevel(self)
        preview_window.title("XML Preview")
        preview_window.geometry("800x600")

        text_widget = scrolledtext.ScrolledText(preview_window, font=('Courier', 10), wrap=tk.WORD)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", xml_string)

        tk.Button(preview_window, text="Close", command=preview_window.destroy,
                 bg=self.accent_color, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(pady=10)

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
                self.status_label.config(text="XML saved successfully!")
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
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_label.config(text="Auto-update running...")

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
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Auto-update stopped")

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

            self.after(0, lambda: self.status_label.config(
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
