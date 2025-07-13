import npyscreen
import datetime
from dateutil.relativedelta import relativedelta

class DateRangeForm(npyscreen.ActionForm):
    def create(self):
        self.name = "📅 Email Date Range Picker"
        
        # Add title
        self.add(npyscreen.TitleText, name="Select Date Range for Email Search", 
                 editable=False, color="STANDOUT")
        
        # Add some spacing
        self.add(npyscreen.FixedText, value="")
        
        # Start Date Section
        self.add(npyscreen.TitleText, name="📅 START DATE", 
                 editable=False, color="GOOD")
        
        self.start_date = self.add(npyscreen.TitleDateCombo, 
                                  name="From Date:", 
                                  value=datetime.date.today() - relativedelta(months=1))
        
        # Add some spacing
        self.add(npyscreen.FixedText, value="")
        
        # End Date Section
        self.add(npyscreen.TitleText, name="📅 END DATE", 
                 editable=False, color="GOOD")
        
        self.end_date = self.add(npyscreen.TitleDateCombo, 
                                name="To Date:", 
                                value=datetime.date.today())
        
        # Add some spacing
        self.add(npyscreen.FixedText, value="")
        
        # Quick preset options
        self.add(npyscreen.TitleText, name="🚀 QUICK PRESETS", 
                 editable=False, color="STANDOUT")
        
        self.preset_options = [
            "Last 7 days",
            "Last 30 days", 
            "Last 3 months",
            "Last 6 months",
            "This month",
            "Last month",
            "This year",
            "Custom range (use dates above)"
        ]
        
        self.preset_select = self.add(npyscreen.TitleSelectOne, 
                                     name="Quick Select:",
                                     values=self.preset_options,
                                     value=[7],  # Default to custom range
                                     max_height=8)
        
        # Add some spacing
        self.add(npyscreen.FixedText, value="")
        
        # Search limit
        self.search_limit = self.add(npyscreen.TitleText, 
                                   name="Max Results:", 
                                   value="50")
        
        # Add some spacing
        self.add(npyscreen.FixedText, value="")
        
        # Instructions
        self.add(npyscreen.TitleText, name="💡 Instructions:", 
                 editable=False, color="LABEL")
        self.add(npyscreen.FixedText, value="• Use arrow keys to navigate")
        self.add(npyscreen.FixedText, value="• Press TAB to move between fields")
        self.add(npyscreen.FixedText, value="• Press ENTER to confirm selection")
        self.add(npyscreen.FixedText, value="• Press Ctrl+C to cancel")
        
    def on_ok(self):
        """Handle OK button press"""
        # Handle preset selection
        if self.preset_select.value:
            preset_index = self.preset_select.value[0]
            if preset_index < 7:  # Not custom range
                self.apply_preset(preset_index)
        
        # Validate dates
        if self.start_date.value > self.end_date.value:
            npyscreen.notify_confirm("❌ Error: Start date must be before end date!", 
                                   title="Invalid Date Range")
            return
        
        # Validate search limit
        try:
            limit = int(self.search_limit.value)
            if limit <= 0:
                raise ValueError()
        except ValueError:
            npyscreen.notify_confirm("❌ Error: Please enter a valid number for max results!", 
                                   title="Invalid Search Limit")
            return
        
        # Store the results
        self.parentApp.date_range_result = {
            'start_date': self.start_date.value,
            'end_date': self.end_date.value,
            'limit': limit,
            'confirmed': True
        }
        
        # Show confirmation
        date_range_str = f"{self.start_date.value.strftime('%B %d, %Y')} to {self.end_date.value.strftime('%B %d, %Y')}"
        npyscreen.notify_confirm(f"✅ Date range selected:\n{date_range_str}\n\nMax results: {limit}", 
                               title="Date Range Confirmed")
        
        # Exit the form
        self.parentApp.setNextForm(None)
    
    def on_cancel(self):
        """Handle Cancel button press"""
        self.parentApp.date_range_result = {'confirmed': False}
        self.parentApp.setNextForm(None)
    
    def apply_preset(self, preset_index):
        """Apply a preset date range"""
        today = datetime.date.today()
        
        if preset_index == 0:  # Last 7 days
            self.start_date.value = today - relativedelta(days=7)
            self.end_date.value = today
        elif preset_index == 1:  # Last 30 days
            self.start_date.value = today - relativedelta(days=30)
            self.end_date.value = today
        elif preset_index == 2:  # Last 3 months
            self.start_date.value = today - relativedelta(months=3)
            self.end_date.value = today
        elif preset_index == 3:  # Last 6 months
            self.start_date.value = today - relativedelta(months=6)
            self.end_date.value = today
        elif preset_index == 4:  # This month
            self.start_date.value = today.replace(day=1)
            self.end_date.value = today
        elif preset_index == 5:  # Last month
            last_month = today - relativedelta(months=1)
            self.start_date.value = last_month.replace(day=1)
            # Last day of last month
            self.end_date.value = today.replace(day=1) - relativedelta(days=1)
        elif preset_index == 6:  # This year
            self.start_date.value = today.replace(month=1, day=1)
            self.end_date.value = today
        
        # Refresh the display
        self.start_date.display()
        self.end_date.display()

class DateRangeApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", DateRangeForm, name="Date Range Picker")
        self.date_range_result = {'confirmed': False}

def get_date_range():
    """Main function to get date range from user"""
    try:
        app = DateRangeApp()
        app.run()
        return app.date_range_result
    except KeyboardInterrupt:
        return {'confirmed': False}
    except Exception as e:
        print(f"❌ Error with date picker: {str(e)}")
        return {'confirmed': False}

if __name__ == "__main__":
    # Test the date range picker
    result = get_date_range()
    if result['confirmed']:
        print(f"✅ Selected date range:")
        print(f"   From: {result['start_date']}")
        print(f"   To: {result['end_date']}")
        print(f"   Limit: {result['limit']}")
    else:
        print("❌ Date range selection cancelled")

