import streamlit as st
import heapq
from datetime import datetime

# ==========================================================
# 1. PAGE CONFIG & DARK MODE DASHBOARD STYLING
# ==========================================================
st.set_page_config(
    page_title="ANIMA Sanctuary Management System",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #F8FAFC !important;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    .stApp p, .stApp label, .stApp span, .stApp div {
        color: #CBD5E1 !important;
    }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    [data-testid="collapsedControl"], button[data-testid="stSidebarCollapseButton"], [data-testid="stHeader"] button {
        visibility: visible !important;
        color: #10B981 !important;
        background-color: #1E293B !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    footer {visibility: hidden;}
    div[data-testid="stMetric"] {
        background-color: #1E293B !important;
        padding: 20px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #334155 !important;
    }
    div[data-testid="stMetricLabel"] p { color: #94A3B8 !important; font-weight: 600 !important; font-size: 0.9rem !important; }
    div[data-testid="stMetricValue"] div { color: #10B981 !important; font-weight: 800 !important; }
    div[data-testid="stForm"] {
        background-color: #1E293B !important;
        border-radius: 16px !important;
        padding: 24px !important;
        border: 1px solid #334155 !important;
    }
    .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }
    .stButton > button {
        background-color: #10B981 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
    }
    .stButton > button:hover { background-color: #34D399 !important; }
    .terminal-card {
        background-color: #020617 !important;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #10B981;
        border: 1px solid #1E293B;
    }
    .terminal-card pre { color: #34D399 !important; font-family: 'Courier New', monospace; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. DSA CLASSES (BST, GENERAL TREE, DLL, STACKS, HEAP)
# ==========================================================

class BSTNode:
    def __init__(self, animal_id, name, species, zone, status="Active / Healthy"):
        self.animal_id = animal_id
        self.name = name
        self.species = species
        self.zone = zone
        self.status = status
        self.left = None
        self.right = None

class TreeNode:
    def __init__(self, node_name):
        self.node_name = node_name
        self.children = []

class DLLNode:
    def __init__(self, animal_id, timestamp, diagnosis, treatment):
        self.animal_id = animal_id
        self.timestamp = timestamp
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, animal_id, diagnosis, treatment):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_node = DLLNode(animal_id, timestamp, diagnosis, treatment)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def get_patient_history(self, animal_id):
        records = []
        curr = self.head
        while curr:
            if curr.animal_id == animal_id:
                records.append({
                    "Timestamp": curr.timestamp,
                    "Diagnosis": curr.diagnosis,
                    "Treatment": curr.treatment
                })
            curr = curr.next
        return records

class FIFOQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, animal_name, species, reason):
        self.queue.append({
            "Name": animal_name,
            "Species": species,
            "Reason": reason,
            "Time": datetime.now().strftime("%H:%M:%S")
        })

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

class MedicalPriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, animal_name, species, priority_level, condition):
        self.count += 1
        heapq.heappush(self.heap, (priority_level, self.count, {
            "Name": animal_name,
            "Species": species,
            "Priority Level": priority_level,
            "Condition": condition
        }))

    def pop(self):
        return heapq.heappop(self.heap)[2] if self.heap else None

    def get_sorted_list(self):
        return [item[2] for item in sorted(self.heap)]

class ActionDualStack:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def record_action(self, action_text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.undo_stack.append(f"[{timestamp}] {action_text}")
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return action
        return None

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return action
        return None

    def get_logs(self):
        return list(reversed(self.undo_stack))

# ==========================================================
# 3. EXPLICIT SORTING & TRAVERSALS
# ==========================================================

def in_order_bst(node, records):
    """Populates registry list in ID order using BST In-Order Traversal."""
    if node is None:
        return
    in_order_bst(node.left, records)
    records.append({
        "Animal ID": node.animal_id,
        "Name": node.name,
        "Species Class": node.species,
        "Habitat Zone": node.zone,
        "Status": node.status
    })
    in_order_bst(node.right, records)

def custom_bubble_sort(records, key, reverse=False):
    """Explicit Bubble Sort algorithm used when user sorts by Name, Species, or Zone."""
    n = len(records)
    arr = list(records)
    for i in range(n):
        for j in range(0, n - i - 1):
            val_a = str(arr[j][key]).lower()
            val_b = str(arr[j+1][key]).lower()
            if (val_a > val_b) if not reverse else (val_a < val_b):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def bst_search(node, target_id):
    curr = node
    steps = 0
    while curr:
        steps += 1
        if curr.animal_id == target_id:
            return curr, steps
        elif target_id < curr.animal_id:
            curr = curr.left
        else:
            curr = curr.right
    return None, steps

# ==========================================================
# 4. INITIALIZATION & PHILIPPINE ENVIRONMENT DATA
# ==========================================================

PHILIPPINE_ZONES = [
    "Lowland Dipterocarp Forest",
    "Mangrove & Coastal Wetland",
    "Mossy Cloud Mountain Forest",
    "Karst Cave System"
]

SPECIES_CLASSES = [
    "Mammals",
    "Birds",
    "Reptiles",
    "Amphibians",
    "Fish",
    "Invertebrates"
]

if "initialized" not in st.session_state:
    st.session_state.bst_root = None
    st.session_state.map_root = TreeNode("ANIMA Sanctuary (Philippines)")
    
    # Build Philippine General Tree Habitat Branches
    st.session_state.map_root.children = [TreeNode(z) for z in PHILIPPINE_ZONES]
    
    st.session_state.health_dll = DoublyLinkedList()
    st.session_state.routine_queue = FIFOQueue()
    st.session_state.triage_heap = MedicalPriorityQueueHeap()
    st.session_state.audit_stacks = ActionDualStack()
    st.session_state.id_counter = 101
    st.session_state.initialized = True

    def seed_initial(name, species, zone_name, zone_idx):
        aid = st.session_state.id_counter
        # BST
        new_bst = BSTNode(aid, name, species, zone_name)
        if not st.session_state.bst_root:
            st.session_state.bst_root = new_bst
        else:
            c = st.session_state.bst_root
            while True:
                if aid < c.animal_id:
                    if not c.left:
                        c.left = new_bst; break
                    c = c.left
                else:
                    if not c.right:
                        c.right = new_bst; break
                    c = c.right
        # General Tree Insertion
        st.session_state.map_root.children[zone_idx].children.append(TreeNode(f"{name} (ID: #{aid})"))
        st.session_state.health_dll.append(aid, "Intake Checkup", "Passed physical evaluation.")
        st.session_state.audit_stacks.record_action(f"Registered '{name}' ({species}) to {zone_name}.")
        st.session_state.id_counter += 1

    # Native Philippine Wildlife Demo Data
    seed_initial("Agila", "Birds", "Mossy Cloud Mountain Forest", 2)
    seed_initial("Tami", "Mammals", "Lowland Dipterocarp Forest", 0)
    seed_initial("Pawikan", "Reptiles", "Mangrove & Coastal Wetland", 1)
    seed_initial("Kabag", "Mammals", "Karst Cave System", 3)
    seed_initial("Agila II", "Birds", "Mossy Cloud Mountain Forest", 2)

    st.session_state.routine_queue.enqueue("Bakawan", "Reptiles", "Rescued from fish trap")
    st.session_state.triage_heap.push("Pilandok", "Mammals", 1, "Severe leg fracture / Emergency Triage")

# ==========================================================
# 5. SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:
    st.title("🐾 ANIMA Sanctuary")
    st.caption("Philippine Wildlife Management System")
    
    selected_page = st.radio(
        "Navigation Menu:",
        [
            "📋 Animal Registry & Map",
            "🩺 Health Log & Medical History",
            "⏳ Admission & Release Queue",
            "📜 Audit Trail & System Log"
        ]
    )
    st.divider()
    st.caption(f"Registered Animals: {st.session_state.id_counter - 101}")
    st.caption(f"Active Eco-Zones: {len(PHILIPPINE_ZONES)}")

# Header Metrics
st.title("ANIMA Sanctuary Operations")
c1, c2, c3 = st.columns(3)
c1.metric("Active Animals", st.session_state.id_counter - 101, delta="BST Indexed")
c2.metric("Intake Queue", len(st.session_state.routine_queue.queue), delta="FIFO Queue")
c3.metric("Next Registry ID", f"#{st.session_state.id_counter}", delta="Auto-Assigned")
st.divider()

# ==========================================================
# 6. FEATURE 1: EXPANDED ANIMAL REGISTRY & MAP
# ==========================================================

if "Animal Registry" in selected_page:
    st.subheader("Sanctuary Animal Registry & Physical Map")
    
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.markdown("### ➕ Register New Animal")
        with st.form("add_animal_form", clear_on_submit=True):
            reg_name = st.text_input("Animal Name (e.g., Agila, Pawikan)")
            reg_species = st.selectbox("Species Class", SPECIES_CLASSES)
            reg_zone = st.selectbox("Philippine Ecosystem Zone", PHILIPPINE_ZONES)
            submit_reg = st.form_submit_button("Complete Registration")
            
            if submit_reg and reg_name:
                zone_idx = PHILIPPINE_ZONES.index(reg_zone)
                aid = st.session_state.id_counter
                
                # BST Insert
                new_bst = BSTNode(aid, reg_name, reg_species, reg_zone)
                if not st.session_state.bst_root:
                    st.session_state.bst_root = new_bst
                else:
                    curr = st.session_state.bst_root
                    while True:
                        if aid < curr.animal_id:
                            if not curr.left:
                                curr.left = new_bst; break
                            curr = curr.left
                        else:
                            if not curr.right:
                                curr.right = new_bst; break
                            curr = curr.right
                
                # General Tree Insert
                st.session_state.map_root.children[zone_idx].children.append(TreeNode(f"{reg_name} (ID: #{aid})"))
                st.session_state.health_dll.append(aid, "Intake Checkup", "Newly registered record created.")
                st.session_state.audit_stacks.record_action(f"Registered '{reg_name}' (#{aid}) into {reg_zone}.")
                
                st.session_state.id_counter += 1
                st.success(f"Registered {reg_name} (ID: #{aid})!")
                st.rerun()

        st.divider()
        
        # SEARCH & MULTI-FILTER ENGINE
        st.markdown("### 🔍 Search & Multi-Filter Engine")
        
        # Collect current records from BST
        all_records = []
        in_order_bst(st.session_state.bst_root, all_records)
        
        search_mode = st.radio("Search Method:", ["Numeric BST Search (O(log n))", "Name & Attribute Filter"], horizontal=True)
        
        if search_mode == "Numeric BST Search (O(log n))":
            search_target = st.number_input("Enter Animal ID", min_value=101, step=1)
            if st.button("Execute BST Search"):
                found_node, steps = bst_search(st.session_state.bst_root, int(search_target))
                if found_node:
                    st.success(f"Located in {steps} step(s): **{found_node.name}** ({found_node.species}) in *{found_node.zone}*")
                    st.session_state.audit_stacks.record_action(f"BST Search ID #{search_target} -> Found '{found_node.name}'.")
                else:
                    st.error(f"Animal ID #{search_target} not found in BST index.")
        else:
            # Name Autocomplete & Attribute Filtering
            existing_names = sorted(list(set([r["Name"] for r in all_records])))
            filter_name = st.selectbox("Select/Type Animal Name:", ["-- All Names --"] + existing_names)
            filter_species = st.selectbox("Filter Species Class:", ["-- All Species --"] + SPECIES_CLASSES)
            filter_zone = st.selectbox("Filter Habitat Zone:", ["-- All Ecosystems --"] + PHILIPPINE_ZONES)
            
            # Filter application logic
            filtered_data = all_records
            if filter_name != "-- All Names --":
                filtered_data = [r for r in filtered_data if r["Name"] == filter_name]
            if filter_species != "-- All Species --":
                filtered_data = [r for r in filtered_data if r["Species Class"] == filter_species]
            if filter_zone != "-- All Ecosystems --":
                filtered_data = [r for r in filtered_data if r["Habitat Zone"] == filter_zone]
                
            st.caption(f"Filtered Results ({len(filtered_data)} record(s) matched):")
            st.dataframe(filtered_data, use_container_width=True)

    with right_col:
        tab1, tab2 = st.tabs(["📋 Global Registry Index", "🌳 Philippine Habitat Map (General Tree)"])
        
        with tab1:
            records = []
            in_order_bst(st.session_state.bst_root, records)
            
            # SORTING CONTROLS
            sort_c1, sort_c2 = st.columns(2)
            with sort_c1:
                sort_key = st.selectbox("Sort Table By:", ["Animal ID (BST Traversal Order)", "Name", "Species Class", "Habitat Zone"])
            with sort_c2:
                sort_order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)
                
            reverse_flag = (sort_order == "Descending")
            
            # Execute sorting
            if sort_key == "Animal ID (BST Traversal Order)":
                display_records = records if not reverse_flag else list(reversed(records))
            else:
                display_records = custom_bubble_sort(records, key=sort_key, reverse=reverse_flag)
                
            st.dataframe(display_records, use_container_width=True)
            
        with tab2:
            st.markdown("### 🌳 Habitat Zone Inspector")
            st.caption("Traverses the General Tree structure (`map_root.children`) to display habitat nodes in tabular form.")
            
            # Dropdown menu to choose specific habitat zone or view all
            selected_zone_filter = st.selectbox(
                "Filter by Habitat Zone Node:", 
                ["-- All Habitat Zones (Full Tree) --"] + PHILIPPINE_ZONES
            )
            
            # Extract tree nodes into tabular format
            tree_table_rows = []
            for zone_node in st.session_state.map_root.children:
                if selected_zone_filter == "-- All Habitat Zones (Full Tree) --" or selected_zone_filter == zone_node.node_name:
                    for animal_node in zone_node.children:
                        # Extract string label from child node
                        full_label = animal_node.node_name
                        parts = full_label.split(" (ID: #")
                        anim_name = parts[0]
                        anim_id = f"#{parts[1].replace(')', '')}" if len(parts) > 1 else "N/A"
                        
                        tree_table_rows.append({
                            "Habitat Zone Node": zone_node.node_name,
                            "Animal ID": anim_id,
                            "Animal Name": anim_name,
                            "General Tree Hierarchy Path": f"ANIMA Root ➔ {zone_node.node_name} ➔ {anim_name}"
                        })
            
            if tree_table_rows:
                st.dataframe(tree_table_rows, use_container_width=True)
            else:
                st.info(f"No animals registered in **{selected_zone_filter}** yet.")

# ==========================================================
# 7. OTHER VIEWS (RETAINED)
# ==========================================================

elif "Health Log" in selected_page:
    st.subheader("Animal Health Logs & Medical History (Doubly Linked List)")
    c_in, c_view = st.columns([1, 2])
    with c_in:
        with st.form("med_form", clear_on_submit=True):
            target_id = st.number_input("Target Animal ID", min_value=101, step=1)
            diagnosis = st.text_input("Diagnosis / Condition")
            treatment = st.text_area("Treatment Administered")
            if st.form_submit_button("Append DLL Node") and diagnosis:
                st.session_state.health_dll.append(int(target_id), diagnosis, treatment)
                st.session_state.audit_stacks.record_action(f"Appended DLL record for ID #{target_id}.")
                st.success(f"Log appended for ID #{target_id}.")
                st.rerun()
    with c_view:
        query_id = st.number_input("Select ID to View History", min_value=101, step=1, key="q_med")
        history = st.session_state.health_dll.get_patient_history(int(query_id))
        st.dataframe(history if history else [], use_container_width=True)

elif "Admission" in selected_page:
    st.subheader("Sanctuary Admission & Triage Pipeline")
    t1, t2 = st.tabs(["⏳ Routine Admission Queue (FIFO Queue)", "🚨 Emergency Medical Triage (Priority Heap)"])
    with t1:
        cin, cv = st.columns([1, 2])
        with cin:
            with st.form("fifo_form", clear_on_submit=True):
                qn = st.text_input("Animal Name")
                qs = st.selectbox("Species Class", SPECIES_CLASSES)
                qr = st.text_area("Reason for Intake")
                if st.form_submit_button("Enqueue Intake") and qn:
                    st.session_state.routine_queue.enqueue(qn, qs, qr)
                    st.session_state.audit_stacks.record_action(f"Enqueued '{qn}' to FIFO Queue.")
                    st.rerun()
        with cv:
            if not st.session_state.routine_queue.is_empty():
                st.dataframe(st.session_state.routine_queue.queue, use_container_width=True)
                if st.button("Dequeue Next Intake"):
                    p = st.session_state.routine_queue.dequeue()
                    st.session_state.audit_stacks.record_action(f"Dequeued intake for '{p['Name']}'.")
                    st.rerun()
            else: st.info("Routine intake queue is empty.")
    with t2:
        hin, hv = st.columns([1, 2])
        with hin:
            with st.form("heap_form", clear_on_submit=True):
                hn = st.text_input("Critical Animal Name")
                hs = st.selectbox("Species Class", SPECIES_CLASSES, key="h_sp")
                hp = st.selectbox("Priority Level", [1, 2, 3], format_func=lambda x: f"Priority {x} - {'Emergency' if x==1 else 'Urgent' if x==2 else 'Routine'}")
                hc = st.text_area("Emergency Condition")
                if st.form_submit_button("Push Heap Node") and hn:
                    st.session_state.triage_heap.push(hn, hs, hp, hc)
                    st.session_state.audit_stacks.record_action(f"Pushed Priority-{hp} case '{hn}' to Heap.")
                    st.rerun()
        with hv:
            sh = st.session_state.triage_heap.get_sorted_list()
            if sh:
                st.dataframe(sh, use_container_width=True)
                if st.button("Pop Highest Priority Emergency Case"):
                    cp = st.session_state.triage_heap.pop()
                    st.session_state.audit_stacks.record_action(f"Popped emergency case '{cp['Name']}'.")
                    st.rerun()
            else: st.info("No emergency cases in heap.")

elif "Audit Trail" in selected_page:
    st.subheader("System Audit Trail & Operations Log (Dual-Stack Undo/Redo)")
    b1, b2, _ = st.columns([1, 1, 2])
    with b1:
        if st.button("⏪ Undo (Pop Stack)") and (u := st.session_state.audit_stacks.undo()):
            st.warning(f"Undid: {u}"); st.rerun()
    with b2:
        if st.button("⏩ Redo (Push Back)") and (r := st.session_state.audit_stacks.redo()):
            st.success(f"Redone: {r}"); st.rerun()
    logs = st.session_state.audit_stacks.get_logs()
    if logs:
        st.markdown(f'<div class="terminal-card"><pre>{"\n".join(logs)}</pre></div>', unsafe_allow_html=True)