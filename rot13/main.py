import cgi
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

text_area = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar</title>
</head>
<body>
    <h1>
        <a href="/">Caesar</a>
    </h1>
    <form method="post">
        <label>Number to Rotate by:</label>
        <input type="number" name="num" required></input>
        <br>
        <textarea name="text" style="height: 100px; width: 400px;">%(output)s
        </textarea>
        <br>
        <input type= "submit">
    </form>
</body>
</html>
"""

def escape_html(text):
    return cgi.escape(text, quote=True)

new_text = ""
rot_num = 0

# Inset input for number of rotation
def caesar(text, num):
    rot = ""
    for x in text:
        ordx = ord(x)
        if ((ordx < 65) or (ordx > 90 and ordx <97) or (ordx > 122)):
            rot = rot + x
        else:
            if x.isupper():
                toprange = 91
                botrange = 65
            else:
                toprange = 123
                botrange = 97

            new_x = (ordx + int(num))% toprange

            if (new_x < botrange):
                new_x = new_x + botrange
                rot = rot + chr(new_x)

            else:
                rot = rot + chr(new_x)

    return escape_html(rot)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, output=""):
        self.response.out.write(text_area % {"output": output})

    def get(self):
        self.write_form()

    def post(self):
        new_text = self.request.get("text")
        rot_num = self.request.get("num")

        output = caesar(new_text, rot_num)

        self.write_form(output)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
