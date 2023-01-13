from scrappers import p02_sx_result_index_scraper
from tkinter import *
from tkmacosx import *

# Window Container:
ui = Tk()
ui.title("Supercross Data Scraper")

def scrapeEventLinks():
  data = p02_sx_result_index_scraper.getEventLinks()  
  return data

# **********************************************
def filterLinks(list):
  output = []
  start = input_start_range.get()
  end = input_end_range.get()

  for year in range(int(start),int(end)+1):
    for item in list:
      if item[0] == str(year):
        output.append(item)
  return output
# **********************************************


def showEventLinks():
  deleteDisplay()
  links = filterLinks(scrapeEventLinks())
  updateDisplay(f" {'YEAR':7} {'ROUND':<8} {'NAME':<25} {'LINK':<50}")
  updateDisplay('-'*125)
  for link in links:
    updateDisplay(f"{link[0]:<11}{link[1]:<15}{link[2]:<30}{link[3]:<30}")

def deleteDisplay():
    display.delete(1.0, END)

def updateDisplay(input):
    display.insert(
        INSERT, f"{input}\n")
    display.tag_configure("left", justify='left')
    display.tag_add("left", 1.0, "end")

step01_frame = Frame(ui)
step01_frame.grid(row=2,column=0, sticky=W)

lbl_step01 = Label(step01_frame, text='Step 01: Scrape links to event result pages:').grid(row=1,column=0,columnspan=4, sticky=W)

lbl_start_range = Label(step01_frame, text='Start Year:').grid(row=2,column=0, sticky=W)
input_start_range = Entry(step01_frame, width=10, bg='white')
input_start_range.grid(row=2,column=1, sticky= W)

lbl_end_range = Label(step01_frame, text='End Year:').grid(row=2,column=2)
input_end_range = Entry(step01_frame, width=10, bg='white')
input_end_range.grid(row=2,column=3, sticky=W)

btn_event_links = Button(step01_frame,text='Scrape!', command = showEventLinks)
btn_event_links.grid(row=2,column=4, sticky=W)

# Output Display
display = Text(ui, width=100, height=20, bg="black",fg="white", font=("Arial", 14))
display.grid(row=100, column=0, columnspan=4)




ui.mainloop()