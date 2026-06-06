from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- Core Game Variables (Mirrored from your original script) ---
game_state = {
    "counter": 0.0,
    "funds": 0.0,
    "CPS": 0.0,
    "discovRate": 1.0,
    "upgrade_rank1_cost": 25.0,
    "fundMin": 1.0,
    "hiredResearchersR1": 0,
    "beaker_cost": 24.0,
    "beakerCount": 0,
    "effRate": 1.0,
    
    # Equipment Counts & Costs
    "eqUp1_count": 0,
    "eqUp2_count": 0,
    "eqUp3_count": 0,
    "equipUp1_cost": 100.0,
    "equipUp2_cost": 150.0,
    "equipUp3_cost": 1000.0,
    
    # Checkbox Toggle State (0 = Off, 1 = On)
    "auto_convert": 0
}

@app.route('/')
def home():
    # Renders the HTML structure, CSS layouts, and JS animation logics
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Science Campaign - Cloud Panel</title>
        <style>
            body { 
                font-family: 'Arial', sans-serif; 
                background-color: #121212; 
                color: #ffffff; 
                margin: 0; 
                padding: 0; 
                overflow: hidden;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
            }
            
            /* Main Screen Configurations */
            #main-container {
                text-align: center;
                margin-top: 40px;
                width: 500px;
                height: 400px;
                position: relative;
            }
            #count-label { color: #0088ff; font-size: 24px; margin: 15px 0; font-weight: bold; }
            #cps-label { color: #00aa55; font-size: 14px; font-style: italic; margin-bottom: 5px; }
            #funds-label { color: #00aa55; font-size: 16px; font-weight: bold; margin-bottom: 25px; }
            
            button {
                font-family: Arial, sans-serif;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: opacity 0.1s;
            }
            button:disabled {
                opacity: 0.4;
                cursor: not-allowed;
            }
            
            #action-button {
                font-size: 14px; padding: 8px 16px; background-color: #f0f0f0; color: black; margin-bottom: 15px;
            }
            #cash-button {
                background-color: #00aa00; color: #ffffff; font-size: 10px; padding: 8px; width: 180px; text-align: center;
            }
            .checkbox-container {
                font-size: 11px; color: #0088ff; font-style: italic; margin: 10px 0;
            }

            /* Sliding Stat Side Panel CSS (replaces Tkinter Frame) */
            #panel-container {
                position: absolute;
                top: 60px;
                right: -420px; /* closed_x geometry */
                width: 450px;
                height: 300px;
                display: flex;
                transition: right 0.2s ease-out;
                z-index: 100;
            }
            #tab-button {
                #tab-button {
                width: 30px; 
                height: 300px; 
                background-color: #0091ff; 
                color: white;
                font-size: 11px; 
                font-weight: bold;
                cursor: pointer;
    
           /* Center the stacked column */
                display: flex; 
                flex-direction: column;
                align-items: center; 
                justify-content: center; 
    
           /* Force the line layout to go vertical */
                writing-mode: vertical-lr;
    
           /* Prevents the browser from tilting the letters sideways */
                text-orientation: upright;
    
           /* Forces a clean line-break behavior per letter if needed */
                word-break: break-all;
    
           /* Gives breathing room between the vertical letters */
                letter-spacing: 4px; 
            }
            }
            #stats-body {
                width: 420px; height: 300px; background-color: #222222; border: 1px solid #555555;
                box-sizing: border-box; padding: 10px; text-align: center;
            }
            .stat-line { font-size: 12px; font-weight: bold; margin: 10px 0; }

            /* Sliding Upgrades Bottom Panel CSS */
            #panel-container2 {
                position: absolute;
                bottom: -320px; /* closed_y geometry */
                left: 0;
                width: 500px;
                height: 350px;
                display: flex;
                flex-direction: column;
                transition: bottom 0.2s ease-out;
                z-index: 50;
            }
            #tab-button2 {
                width: 100%; height: 30px; background-color: #0091ff; color: white;
                font-size: 11px; text-align: center; line-height: 30px; cursor: pointer;
            }
            #upgrd-body {
                width: 100%; height: 320px; background-color: #222222; border-top: 1px solid #555555;
                overflow-y: auto; box-sizing: border-box; padding: 15px; position: relative;
            }
            
            /* Upgrade Layout Grid placement matching .place() offsets */
            .up-btn {
                position: absolute; width: 210px; height: 50px; font-size: 11px;
                background-color: #0091ff; color: white; padding: 5px; text-align: center;
            }
            #up-btn-1 { left: 20px; top: 30px; }
            #up-btn-2 { left: 250px; top: 30px; }
            #up-btn-3 { left: 20px; top: 100px; }
            #up-btn-4 { left: 250px; top: 100px; }
            #up-btn-5 { left: 20px; top: 180px; }
        </style>
    </head>
    <body>

        <div id="main-container">
            <div id="count-label">Discovery Points: 0.0</div>
            <div id="cps-label">Per Second: 0</div>
            <div id="funds-label">$0.00</div>
            
            <button id="action-button" onclick="triggerAction('/count')">Discovery</button>
            
            <div class="checkbox-container">
                <input type="checkbox" id="auto-convert-check" onchange="toggleAutoConvert(this.checked)">
                <label for="auto-convert-check">Auto-Convert Points to Funds</label>
            </div>
            
            <button id="cash-button" onclick="triggerAction('/cashInFunds')">Cash in Points for funds (+0.25)<br>Cost: 1 Point</button>

            <div id="panel-container">
                <div id="tab-button" onclick="toggleStats()">
                    <span class="arrow">◀</span>STATS
                </div>
                <div id="stats-body">
                    <div style="font-size: 13px; font-weight: bold; margin: 10px 0;">LAB OVERVIEW</div>
                    <div class="stat-line" style="color: #ffaa00;" id="lbl-researchers">Junior Researchers:<br>0</div>
                    <div class="stat-line" style="color: #00e5ff;" id="lbl-beakers">Glass Beakers:<br>0</div>
                    <div class="stat-line" style="color: #00e5ff;" id="lbl-equip1">Equipment Upgrades:<br>0</div>
                    <div class="stat-line" style="color: #00e5ff;" id="lbl-equip2">Chemical Centerfuge:<br>0</div>
                    <div class="stat-line" style="color: #00e5ff;" id="lbl-equip3">Computer Arrays:<br>0</div>
                </div>
            </div>

            <div id="panel-container2">
                <div id="tab-button2" onclick="toggleUpgrades()">🔺 UPGRADES 🔺</div>
                <div id="upgrd-body">
                    <button class="up-btn" id="up-btn-1" onclick="triggerAction('/buyCPS_upgrade')">Hire Researchers (+1 CPS)<br>Cost: 25 Pts</button>
                    <button class="up-btn" id="up-btn-2" onclick="triggerAction('/buy_Beaker')">Buy Glass Beakers (+0.5x Multiplier)<br>Cost: $24.00</button>
                    <button class="up-btn" id="up-btn-3" onclick="triggerAction('/buy_eqUp1')">Advanced Lab Equip (+0.5x Efficiency)<br>Cost: $100</button>
                    <button class="up-btn" id="up-btn-4" onclick="triggerAction('/buy_eqUp2')">Chemical Centrifuge (+3.5 CPS)<br>Cost: $150</button>
                    <button class="up-btn" id="up-btn-5" onclick="triggerAction('/buy_eqUp3')">Computer Array (+2.5 CPS)<br>Cost: $1000</button>
                </div>
            </div>
        </div>

        <script>
            let statsOpen = false;
            let upgradesOpen = false;

            // Interface Control (Sliding Panel Mechanics)
            function toggleStats() {
                const p = document.getElementById('panel-container');
                const btn = document.getElementById('tab-button');
                // Layer management logic ensuring clicking stats brings it forward
                p.style.zIndex = "101";
                document.getElementById('panel-container2').style.zIndex = "50";
                
                if(statsOpen) {
                    p.style.right = "-420px";
                    btn.innerHTML = "◀<br>S<br>T<br>A<br>T<br>S";
                    statsOpen = false;
                } else {
                    p.style.right = "10px";
                    btn.innerHTML = "▶<br>H<br>I<br>D<br>E";
                    statsOpen = true;
                }
            }

            function toggleUpgrades() {
                const p = document.getElementById('panel-container2');
                const btn = document.getElementById('tab-button2');
                p.style.zIndex = "100";
                document.getElementById('panel-container').style.zIndex = "50";
                
                if(upgradesOpen) {
                    p.style.bottom = "-320px";
                    btn.innerText = "🔺 UPGRADES 🔺";
                    upgradesOpen = false;
                } else {
                    p.style.bottom = "20px";
                    btn.innerText = "🔻 HIDE 🔻";
                    upgradesOpen = true;
                }
                // Maintain zIndex stacking hierarchy so side panel handle remains interactable
                document.getElementById('panel-container').style.zIndex = "101";
            }

            // Syncing with Web Port API endpoints
            function triggerAction(endpoint) {
                fetch(endpoint, {method: 'POST'})
                    .then(res => res.json())
                    .then(data => updateUI(data));
            }

            function toggleAutoConvert(isActive) {
                fetch('/toggle_auto', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({value: isActive ? 1 : 0})
                });
            }

            function updateUI(state) {
                let effCPS = state.CPS * state.discovRate;
                
                // Labels Sync
                document.getElementById('count-label').innerText = `Discovery Points: ${state.counter.toFixed(1)}`;
                document.getElementById('funds-label').innerText = `$${state.funds.toFixed(2)}`;
                
                if(state.beakerCount > 0) {
                    document.getElementById('cps-label').innerHTML = `Per Second: <br>${effCPS.toFixed(1)} (${state.discovRate}x Boost)`;
                } else {
                    document.getElementById('cps-label').innerHTML = `Per Second: <br>${state.CPS}`;
                }

                // Stats Dashboard Updates
                document.getElementById('lbl-researchers').innerHTML = `Junior Researchers: <br>${state.hiredResearchersR1}`;
                document.getElementById('lbl-beakers').innerHTML = `Glass Beakers: <br>${state.beakerCount}`;
                document.getElementById('lbl-equip1').innerHTML = `Equipment Upgrades: <br>${state.eqUp1_count}`;
                document.getElementById('lbl-equip2').innerHTML = `Chemical Centerfuge: <br>${state.eqUp2_count}`;
                document.getElementById('lbl-equip3').innerHTML = `Computer Arrays: <br>${state.eqUp3_count}`;

                // Dynamic Button State Rules
                document.getElementById('up-btn-1').disabled = (state.counter < state.upgrade_rank1_cost);
                document.getElementById('up-btn-2').disabled = (state.funds < state.beaker_cost);
                document.getElementById('cash-button').disabled = (state.counter < state.fundMin);
                document.getElementById('up-btn-3').disabled = (state.funds < state.equipUp1_cost);
                document.getElementById('up-btn-4').disabled = (state.funds < state.equipUp2_cost);
                document.getElementById('up-btn-5').disabled = (state.funds < state.equipUp3_cost);
            }

            // Automated Game Sync Engine loop (replaces root.after)
            setInterval(() => {
                fetch('/loop', {method: 'POST'})
                    .then(res => res.json())
                    .then(data => updateUI(data));
            }, 1000);
        </script>
    </body>
    </html>
    ''')

# --- Cloud Server Route Operations ---

@app.route('/count', methods=['POST'])
def run_count():
    game_state["counter"] += 0.5
    return jsonify(game_state)

@app.route('/cashInFunds', methods=['POST'])
def run_cash():
    if game_state["counter"] >= game_state["fundMin"]:
        game_state["counter"] -= 1
        game_state["funds"] += 0.25
        if game_state["counter"] >= 20:
            game_state["counter"] -= 4
            game_state["funds"] += 1
    return jsonify(game_state)

@app.route('/buyCPS_upgrade', methods=['POST'])
def run_cps():
    if game_state["counter"] >= game_state["upgrade_rank1_cost"]:
        game_state["counter"] -= game_state["upgrade_rank1_cost"]
        game_state["CPS"] += 1
        game_state["hiredResearchersR1"] += 1
    return jsonify(game_state)

@app.route('/buy_Beaker', methods=['POST'])
def run_beaker():
    if game_state["funds"] >= game_state["beaker_cost"]:
        game_state["funds"] -= game_state["beaker_cost"]
        game_state["discovRate"] += 0.5
        game_state["beakerCount"] += 1
    return jsonify(game_state)

@app.route('/buy_eqUp1', methods=['POST'])
def run_equp1():
    if game_state["funds"] >= game_state["equipUp1_cost"]:
        game_state["funds"] -= game_state["equipUp1_cost"]
        game_state["eqUp1_count"] += 1
        game_state["effRate"] += 0.5
        game_state["discovRate"] *= game_state["effRate"]
    return jsonify(game_state)

@app.route('/buy_eqUp2', methods=['POST'])
def run_equp2():
    if game_state["funds"] >= game_state["equipUp2_cost"]:
        game_state["funds"] -= game_state["equipUp2_cost"]
        game_state["eqUp2_count"] += 1
        game_state["CPS"] += 3.5
    return jsonify(game_state)

@app.route('/buy_eqUp3', methods=['POST'])
def run_equp3():
    if game_state["funds"] >= game_state["equipUp3_cost"]:
        game_state["funds"] -= game_state["equipUp3_cost"]
        game_state["eqUp3_count"] += 1
        game_state["CPS"] += 2.5
    return jsonify(game_state)

@app.route('/toggle_auto', methods=['POST'])
def toggle_auto():
    data = request.get_json()
    game_state["auto_convert"] = data.get("value", 0)
    return jsonify(success=True)

@app.route('/loop', methods=['POST'])
def run_loop():
    # Idle processing logic executed once every second
    if game_state["CPS"] > 0:
        effective_cps = game_state["CPS"] * game_state["discovRate"]
        game_state["counter"] += effective_cps
        
    if game_state["auto_convert"] == 1:
        for _ in range(5):
            if game_state["counter"] >= game_state["fundMin"]:
                # inline conversion engine step
                game_state["counter"] -= 1
                game_state["funds"] += 0.25
                if game_state["counter"] >= 20:
                    game_state["counter"] -= 4
                    game_state["funds"] += 1
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
