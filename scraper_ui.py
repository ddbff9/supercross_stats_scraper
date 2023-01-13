from scrappers import p02_sx_result_index_scraper
from tkinter import *
from tkmacosx import *

# Window Container:
ui = Tk()
ui.title("Supercross Data Scraper")

def scrapeEventLinks():
  deleteDisplay()
  updateDisplay(f"{'YEAR':7} {'ROUND':<8} {'NAME':<25} {'LINK':<50}")
  data = p02_sx_result_index_scraper.getEventLinks()
  for round in data:
    year = input_start_range.get()
    if round[0] == year:
      round = round[1]
      name = round[2]
      link_url = round[3]
      updateDisplay(f"{year:<9}{round:<14}{name:<30}{link_url:<30}")
  
  return data

def showEventLinks():
  deleteDisplay()
  links = scrapeEventLinks()
  deleteDisplay()
  updateDisplay(f"{'YEAR':7} {'ROUND':<8} {'NAME':<25} {'LINK':<50}")
  updateDisplay('-'*125)
  for link in links:
    year = link[0]
    round = link[1]
    name = link[2]
    link_url = link[3]
    updateDisplay(f"{year:<9}{round:<14}{name:<30}{link_url:<30}")

# print(f"{'Location: ' + location:<25} Revision: {revision}")
# print(f"{'District: ' + district:<25} Date: {date}")
# print(f"{'User: ' + user:<25} Time: {time}")

def deleteDisplay():
    display.delete(1.0, END)

def updateDisplay(input):
    display.insert(
        INSERT, f"{input}\n")
    display.tag_configure("left", justify='left')
    display.tag_add("left", 1.0, "end")

row2 = Frame(ui)
row2.grid(row=2,column=0, sticky=W)

lbl_step01 = Label(row2, text='Step 01: Extract Event Details from Racer X Vault').grid(row=1,column=0,columnspan=4, sticky=W)
lbl_start_range = Label(row2, text='Start Year:').grid(row=2,column=0, sticky=W)
input_start_range = Entry(row2, width=10, bg='white').grid(row=2,column=1, sticky= W)
lbl_end_range = Label(row2, text='End Year:').grid(row=2,column=2)
input_end_range = Entry(row2, width=10, bg='white').grid(row=2,column=3, sticky=W)

row3 = Frame(ui)
row3.grid(row=3,column=0, sticky=W)
# Scrape links to event result pages:
lbl_scrape_event_links = Label(row3,text='Scrape links to event result pages: ')
lbl_scrape_event_links.grid(row=0,column=0, sticky=W)

btn_event_links = Button(row3,text='Scrape!', command = scrapeEventLinks)
btn_event_links.grid(row=0,column=2, sticky=W)

btn_event_links = Button(row3,text='View Links', command = showEventLinks)
btn_event_links.grid(row=0,column=3, sticky= W)

# Output Display
display = Text(ui, width=100, height=20, bg="black",fg="white", font=("Arial", 14))
display.grid(row=100, column=0, columnspan=4)




ui.mainloop()