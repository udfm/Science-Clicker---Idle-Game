import tkinter as tk
import os

#game variables
counter = 0
funds = 0
CPS = 0
discovRate = 1
upgrade_rank1_cost = 25
fundMin = 1
hiredResearchersR1 = 0
beaker_cost = 24
beakerCount = 0
effRate = 1

#upgrades equipment
eqUp1_count = 0
eqUp2_count = 0
eqUp3_count = 0
equipUp1_cost = 100
equipUp2_cost = 150
equipUp3_cost = 1000

#window setup
winWidth = 500
winHeight = 400

#panel boolean
panelIsOpen = False
panelIsOpen_U = False

#stats panel
panel_width = 450
closed_x = winWidth - 30
open_x = winWidth - panel_width - 10

#upgrades panel
panelHeight_U = 350
closed_y = winHeight - 30
open_y = winHeight - panelHeight_U

        
#count function
def count():
    global counter
    counter += 0.5
    update_ui()
    
#cash in money to buy items and equipment
def cashInFunds():
    global counter, funds, fundMin
    if counter >= fundMin:
        counter -= 1
        funds += 0.25
        if counter >= 20:
            counter -= 4
            funds += 1
        update_ui()

#upgrade purchase function Rank 1 CPS
#make sure researchers only work if there is more than $5 subtract $0.5 per sec
#if $ is insufficient then stop working until sufficient
def buyCPS_upgrade():
    global CPS, counter, hiredResearchersR1
    if counter >= upgrade_rank1_cost:
        counter -= upgrade_rank1_cost
        CPS += 1
        hiredResearchersR1 += 1
        update_ui()

def buy_Beaker():
    global CPS, funds, discovRate, beakerCount
    if funds >= beaker_cost:
        funds -= beaker_cost
        discovRate += 0.5
        beakerCount += 1
        update_ui()

def buy_eqUp1():
    global eqUp1_count, discovRate, equipUp1_cost, funds, effRate
    if funds >= equipUp1_cost:
        funds -= equipUp1_cost
        eqUp1_count += 1
        effRate += 0.5
        discovRate *= effRate
        update_ui()

def buy_eqUp2():
    global eqUp2_count, CPS, equipUp2_cost, funds 
    if funds >= equipUp2_cost:
        funds -= equipUp2_cost
        eqUp2_count += 1
        CPS += 3.5
        update_ui()
    
def buy_eqUp3():
    global eqUp3_count, CPS, equipUp3_cost, funds
    if funds >= equipUp3_cost:
        funds -= equipUp3_cost
        eqUp3_count += 1
        CPS += 2.5
        update_ui()
        
        
#UI update function
def update_ui():
    effective_cps = CPS * discovRate
    
    count_label.config(text=f"Discovery Points: {counter:.1f}")
    funds_label.config(text=f"${funds:.2f}")
    
    if beakerCount > 0:
        CPS_label.config(text=f"Per Second: \n{effective_cps: .1f} ({discovRate}x Boost)")
    else:
        CPS_label.config(text=f"Per Second: \n{CPS}")
    
    beakerCount_label.config(text=f"Glass Beakers: \n{beakerCount}")
    AdvancedLabEquip_label.config(text=f"Equipment Upgrades: \n{eqUp1_count}")
    chemCenterfuge_label.config(text=f"Chemical Centerfuge: \n{eqUp2_count}")
    computerArray_label.config(text=f"Computer Arrays: \n{eqUp3_count}")
    hiredResearchersR1_label.config(text=f"Junior Researchers: \n{hiredResearchersR1}")
    
    # Button state triggers
    if counter < upgrade_rank1_cost:
        upgrade_button.config(state="disabled")
    else:
        upgrade_button.config(state="normal")
    if funds < beaker_cost:
        Beaker_upgrade_Button.config(state="disabled")
    else:
        Beaker_upgrade_Button.config(state="normal")
    if counter < fundMin:
        cash_button.config(state="disabled")
    else:
        cash_button.config(state="normal")
    if funds < equipUp1_cost:
        equip_upgrade1.config(state="disabled")
    else:
        equip_upgrade1.config(state="normal")
    if funds < equipUp2_cost:
        equip_upgrade2.config(state="disabled")
    else:
        equip_upgrade2.config(state="normal")
    if funds < equipUp3_cost:
        equip_upgrade3.config(state="disabled")
    else:
        equip_upgrade3.config(state="normal")

def autoClick_loop():
    global counter
    
    # 1. Generate normal core points from idle production
    if CPS > 0:
        effective_cps = CPS * discovRate
        counter += effective_cps
        
    # 2. Automated conversion step if the checkbox toggle is active
    if auto_convert_var.get() == 1:
        # If the user has points to spare, auto-convert up to 5 points every second
        for _ in range(5):
            if counter >= fundMin:
                cashInFunds()
    
    update_ui()
    root.after(1000, autoClick_loop)

def animateSlide(widget,dimension, current_pos, target_pos, step):
    if current_pos != target_pos:
        next_pos = current_pos + step
        if (step > 0 and next_pos > target_pos) or (step < 0 and next_pos < target_pos):
            next_pos = target_pos
        if dimension == "x":
            widget.place(x=next_pos)
        elif dimension == "y":
            widget.place(y=next_pos)
        root.after(10, lambda: animateSlide(widget, dimension, next_pos, target_pos, step))

def togglePanel():
    global panelIsOpen
    panel_container.lift()
    if panelIsOpen:
        animateSlide(panel_container, "x", open_x, closed_x, step=10)
        tabButton.config(text="◀\nS\nT\nA\nT\nS")
        panelIsOpen = False
    else:
        animateSlide(panel_container, "x", closed_x, open_x, step=-10)
        tabButton.config(text="▶\nH\nI\nD\nE")
        panelIsOpen = True

def togglePanel_U():
    global panelIsOpen_U
    panel_container2.lift()
    if panelIsOpen_U:
        animateSlide(panel_container2, "y", open_y, closed_y, step=10)
        tabButton2.config(text="🔺UPGRADES🔺")
        panelIsOpen_U = False
    else:
        animateSlide(panel_container2, "y", closed_y, open_y, step=-10)
        tabButton2.config(text="🔻HIDE🔻")
        panelIsOpen_U = True
    panel_container.lift()

#initial setup
root = tk.Tk()
root.title("Science Campaign")
root.geometry("500x400")

'''Labels'''
count_label = tk.Label(root, fg= "blue", pady= "25")
count_label.pack()

CPS_label = tk.Label(root, fg="darkgreen", font=("Arial", 12, "italic"))
CPS_label.pack(pady=5)

funds_label = tk.Label(root, fg="darkgreen", font=("Arial", 12, "bold"))
funds_label.pack(pady=25)
funds_label.place(x=8, y=25)

'''main buttons'''
actionButton = tk.Button(root, text=f"Discovery", command=count, padx=5, pady=5)
actionButton.pack(pady=15)

# --- NEW AUTO CONVERT TOGGLE UI elements ---
auto_convert_var = tk.IntVar()
auto_convert_check = tk.Checkbutton(
    root, 
    text="Auto-Convert Points to Funds", 
    variable=auto_convert_var,
    font=("Arial", 8, "italic"),
    fg="blue"
)
auto_convert_check.place(x=10, y=175)

#cash in button
cash_button = tk.Button(
    root,
    text=f"Cash in Points for funds (+0.25)\nCost: 1 Point",
    command=cashInFunds,
    fg="darkgreen",
    bg="green",
    font=("Arial", 7, "bold"),
    padx=5,
    pady=5
)
cash_button.place(x=10,y=205)

'''Upgrade panel'''
panel_container2 = tk.Frame(root)
panel_container2.place(x=0, y=closed_y, width=winWidth, height=panelHeight_U)

tabButton2 = tk.Button(panel_container2, text="🔺 UPGRADES 🔺", command=togglePanel_U, bg="#0091ff", fg="white", font=("Arial", 8, "bold"), bd=0, relief="flat")
tabButton2.pack(fill="x")

upgrd_body = tk.Frame(panel_container2, bg="#222222", bd=1, relief="solid")
upgrd_body.pack(fill="both", expand=True)

upgrade_canvas = tk.Canvas(upgrd_body, bg="#222222", highlightthickness=0)
upgrade_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(upgrd_body, orient="vertical", command=upgrade_canvas.yview)
scrollbar.pack(side="right", fill="y")
upgrade_canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(upgrade_canvas, bg="#222222")
canvas_frame_window = upgrade_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=winWidth-20)

def configure_scroll_region(event):
    upgrade_canvas.configure(scrollregion=upgrade_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scroll_region)

def _on_mousewheel(event):
    upgrade_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
upgrade_canvas.bind_all("<MouseWheel>", _on_mousewheel)

upgrade_button = tk.Button(scrollable_frame, text="Hire Researchers (+1 CPS)\nCost: 25 Pts", command=buyCPS_upgrade, fg="white", bg="#0091ff", font=("Arial", 9, "bold"), padx=5, pady=5)
upgrade_button.place(x=20, y=30, width=210, height=50)

Beaker_upgrade_Button = tk.Button(scrollable_frame, text=f"Buy Glass Beakers (+0.5x Multiplier)\nCost: ${beaker_cost}", command=buy_Beaker, fg="white", bg="#0091ff", font=("Arial", 9, "bold"), padx=5, pady=5)
Beaker_upgrade_Button.place(x=250, y=30, width=210, height=50)

equip_upgrade1 = tk.Button(scrollable_frame, text="Advanced Lab Equip (+0.5x Efficiency)\nCost: $100", command=buy_eqUp1, fg="white", bg="#0091ff", font=("Arial", 9, "bold"))
equip_upgrade1.place(x=20, y=100, width=210, height=50)

equip_upgrade2 = tk.Button(scrollable_frame, text="Chemical Centrifuge (+3.5 CPS)\nCost: $150", command=buy_eqUp2, fg="white", bg="#0091ff", font=("Arial", 9, "bold"))
equip_upgrade2.place(x=250, y=100, width=210, height=50)

equip_upgrade3 = tk.Button(scrollable_frame, text="Computer Array (+2.5 CPS)\nCost: $1000", command=buy_eqUp3, fg="white", bg="#0091ff", font=("Arial", 9, "bold"))
equip_upgrade3.place(x=20, y=180, width=210, height=50)

def set_interior_height():
    scrollable_frame.config(height=400) 
root.after(10, set_interior_height)

'''Sliding stat panel'''
#fix overlap layer bug later
panel_container = tk.Frame(root)
panel_container.place(x=closed_x, y=60, width=panel_width + 10, height=300)

tabButton = tk.Button(panel_container, text="◀\nS\nT\nA\nT\nS", command=togglePanel, bg="#0091ff", fg="white", font=("Arial", 8, "bold"), bd=0, relief="flat")
tabButton.place(x=0, y=0, width=30, height=300)

stats_body = tk.Frame(panel_container, bg="#222222", bd=1, relief="solid")
stats_body.place(x=30, y=0, width=panel_width, height=350)

stats_title = tk.Label(stats_body, text="LAB OVERVIEW", bg="#222222", fg="white", font=("Arial", 10, "bold"))
stats_title.pack(pady=10)

hiredResearchersR1_label = tk.Label(stats_body, fg="#ffaa00", bg="#222222", font=("Arial", 9, "bold"))
hiredResearchersR1_label.pack(pady=5)

beakerCount_label = tk.Label(stats_body, fg="#00e5ff", bg="#222222", font=("Arial", 9, "bold"))
beakerCount_label.pack(pady=5)

AdvancedLabEquip_label = tk.Label(stats_body, fg="#00e5ff", bg="#222222", font=("Arial", 9, "bold"))
AdvancedLabEquip_label.pack(pady=5)

chemCenterfuge_label = tk.Label(stats_body, fg="#00e5ff", bg="#222222", font=("Arial", 9, "bold"))
chemCenterfuge_label.pack(pady=5)

computerArray_label = tk.Label(stats_body, fg="#00e5ff", bg="#222222", font=("Arial", 9, "bold"))
computerArray_label.pack(pady=5)

#program execution
update_ui()
autoClick_loop()
root.mainloop()
