from scrappers import p02_sx_result_index_scraper
from tkinter import *
from tkmacosx import *

# Window Container:
ui = Tk()
ui.title("Supercross Data Scraper")

def scrapeEventLinks():
  data = p02_sx_result_index_scraper.getEventLinks()
  scraped_links = data['Links']
  errors = data['Errors']

  updateDisplay(f"Created {len(scraped_links)} links")

  for error in errors:
    updateDisplay(error)
  
  return scraped_links

def showEventLinks():
  deleteDisplay()
  links = scrapeEventLinks()
  deleteDisplay()
  for link in links:
    updateDisplay(link[1])

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