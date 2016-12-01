import webapp2

#validate month
#array if valid months
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

#dictionary of first three letters of valid months
#and relate to array
month_abbvs = dict((m[:3].lower(), m) for m in months)

#method: if first three letters of valid month is in
#dictionary return month from array
def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

#validate day
#method for if 0<day<31 return day
def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

#validate year
#method for if 1900<year<2016 return year
def valid_year(year):
    if year and year.isdigit():
        year =int(year)
        if year > 1900 and year < 2016:
            return year

#built in method to escape html in form
import cgi
def escape_html(s):
    return cgi.escape(s, quote = True)

#variable containing form html as text
form="""
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day (DD)
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year (YYYY)
        <input type="text" name="year" value="%(year)s">
    </label>
        <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

#Class for form, verification and error message
class MainPage(webapp2.RequestHandler):
    #create form and escape html
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    #get created form
    def get(self):
        self.write_form()

    #post corrected form
    def post(self):
        #assign variables for form fill in
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        #convert variables for use in validation
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        #return validation
        #if not valid return form with values and error message
        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
                            user_month, user_day, user_year)

        #if form is valid redirect to /thanks
        else:
            self.redirect("/thanks")

#create class for redirect page
class ThanksHandler(webapp2.RequestHandler):
    #get redirect page
    def get(self):
        self.response.out.write("Thanks! That's a totally valid date!")

#handlers for both classes
app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler)
    ],
    debug=True)
