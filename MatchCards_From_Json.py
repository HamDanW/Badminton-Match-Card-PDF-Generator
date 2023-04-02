import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import textwrap
from reportlab.platypus import Table, TableStyle

# Load match card data from JSON file
with open('matchSchedule.json') as f:
    match_cards = json.load(f)
    
def abbreviate(team):
    cap = 20
    isdouble=False
    res = ""
    
    if "+" in team:
        isdouble= True
    
    if len(team)> cap:
        if isdouble:
            # ex: Oliver Wu+Sumaswara Chinthalapati[5/8]
            players = team.split("+")
            # ["Oliver Wu", "Sumaswara Chinthalapati[5/8]"]
            for p in range(len(players)):
                players[p]=players[p].split(" ")
            # [{{"Oliver"}, {"Wu"}}, {{"Sumaswara},{Chinthalapati[5/8]"}}]
            for i in players[0]:
                if i == players[0][-1]:
                    res += i
                else:
                    res = res + i[0] + ". "
            res += " + "
            for i in players[1]:
                if i == players[1][-1]:
                    res += i
                else:
                    res = res + i[0] + ". "
        else:
            # ex Ridhiman Krishna Patwari
            player = team.split(" ")
            # ["Ridhiman", "Krishna", "Patwari"]
            for i in player:
                if i == player[-1]:
                    res += i
                else:
                    res = res + i[0] + ". "
        return res;
    return team

# Define function to draw a match card
def draw_match_card(canvas, x, y, match):
    # Draw the match name, date, and time
    time = match[0]
    event = match[1]
    round = match[2]
    name = match[3]
    teamslist = name.split(" vs. ")
    for i in range(len(teamslist)):
        if "or" in teamslist[i]:
            teamslist[i] = ""
    if teamslist[0] == "" and teamslist[1] == "":
        name = ""
    elif teamslist[0] == "" or teamslist[1] == "":
        name = teamslist[0] + " vs. " + teamslist[1]
        
    teamslist[0] = abbreviate(teamslist[0])
    teamslist[1] = abbreviate(teamslist[1])
    canvas.setFont("Helvetica", 10)

    canvas.drawString(x, y, round)
    canvas.drawString(x, y-0.25*inch, f"Date: Saturday")
    canvas.drawString(x, y-0.5*inch, f"Time: {time}")
    canvas.drawString(x+2*inch, y, f"Event: {event}")
    
    teams = textwrap.wrap(name, width=40)
    for i, line in enumerate(teams):
        canvas.drawString(x, y-(i+1)*0.25*inch-0.75*inch+.25*inch, line)

    # Draw the table
    canvas.saveState()
    canvas.translate(x+.25*inch, y-1.5*inch)
    canvas.scale(1, 1)  # Scale down the table by 50%
    canvas.setFontSize(8)
    if len(teamslist[0])>=16:
        team1 = textwrap.wrap(teamslist[0], width=16)
        for i, line in enumerate(team1):
            canvas.drawString(-0.25*inch, -.5*inch-(i)*0.25*inch, line)
    else:
        canvas.drawString(-0.25*inch, -.5*inch, teamslist[0])
        
    # canvas.drawString(-0.25*inch, -0.5*inch, teamslist[0])
    canvas.line(-.25*inch,-.8*inch,3.25*inch, -.8*inch)
    #vertical lines
    canvas.line(1.75*inch,-1.4*inch,1.75*inch, 0.15*inch)
    canvas.line(2.75*inch,-1.4*inch,2.75*inch, 0.15*inch)
    canvas.drawString(1*inch, 0, "game 1")
    canvas.drawString(2*inch, 0, "game 2")
    canvas.drawString(3*inch, 0, "game 3")
    #canvas.drawString(-0.25*inch, -1*inch, teamslist[1])
    if len(teamslist[1])>=16:
        team1 = textwrap.wrap(teamslist[1], width=16)
        for i, line in enumerate(team1):
            canvas.drawString(-0.25*inch, -1*inch-(i)*0.25*inch, line)
    else:
        canvas.drawString(-0.25*inch, -1*inch, teamslist[1])
    canvas.restoreState()
    
     

# Create a new PDF document
pdf = canvas.Canvas('match_cards.pdf', pagesize=letter)

# Define the dimensions of the match card area
card_width = 4.25*inch
card_height = 3.5*inch

# Calculate the number of cards that can fit on a single page
cards_per_page = 6

# Calculate the number of pages needed to display all of the matches
total_cards = sum([len(match_cards[day]) for day in match_cards])
total_pages = int(total_cards / cards_per_page) + (total_cards % cards_per_page > 0)

# Iterate over the match cards and draw them on the PDF document
x = 0.5*inch
y = 10*inch
i = 0
for day in match_cards:
    for match in match_cards[day]:
        # Draw the match card
        draw_match_card(pdf, x, y, match)

        # Move to the next column
        if i % 2 == 0:
            x += card_width
        else:
            x -= card_width
            y -= card_height

            # Move to the next row if we're at the end of a row
            if i % cards_per_page == cards_per_page - 1:
                pdf.showPage()
                x = 0.5*inch
                y = 10*inch

        i += 1

# Save the PDF document
pdf.save()