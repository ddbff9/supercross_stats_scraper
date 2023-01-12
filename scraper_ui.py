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


title = Label(ui,text='Supercross Data Scraper')
title.grid(row=0, column=0)

# Scrape links to event result pages:
lbl_scrape_event_links = Label(ui,text='Scrape links to event result pages: ')
lbl_scrape_event_links.grid(row=1,column=0)

btn_event_links = Button(ui,text='Scrape!', command = scrapeEventLinks)
btn_event_links.grid(row=1,column=1)

# See Event Links:
btn_event_links = Button(ui,text='View Links', command = showEventLinks)
btn_event_links.grid(row=1,column=2)

# Output Display
display = Text(ui, width=100, height=20, bg="black",fg="white", font=("Arial", 14))
display.grid(row=100, column=0, columnspan=4)




ui.mainloop()