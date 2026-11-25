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
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. DSA CLASSES (BST, GENERAL TREE, DLL, PRIORITY HEAP)
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

class MedicalPriorityQueueHeap:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, animal_name, species, zone, priority_level, condition):
        self.count += 1
        heapq.heappush(self.heap, (priority_level, self.count, {
            "Name": animal_name,
            "Species": species,
            "Zone": zone,
            "Priority Level": priority_level,
            "Condition": condition
        }))

    def pop(self):
        return heapq.heappop(self.heap)[2] if self.heap else None

    def get_sorted_list(self):
        return [item[2] for item in sorted(self.heap)]

# ==========================================================
# 3. EXPLICIT SORTING, TRAVERSALS & DELETION ALGORITHMS
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

def min_value_node(node):
    """Finds the in-order successor (smallest node in right subtree)."""
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_bst(root, target_id):
    """Standard Recursive Binary Search Tree Deletion Algorithm."""
    if root is None:
        return root
    if target_id < root.animal_id:
        root.left = delete_bst(root.left, target_id)
    elif target_id > root.animal_id:
        root.right = delete_bst(root.right, target_id)
    else:
        # Case 1 & 2: Node with 0 or 1 child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        # Case 3: Node with 2 children
        temp = min_value_node(root.right)
        root.animal_id = temp.animal_id
        root.name = temp.name
        root.species = temp.species
        root.zone = temp.zone
        root.status = temp.status
        root.right = delete_bst(root.right, temp.animal_id)
    return root

def delete_from_general_tree(map_root, target_id):
    """Removes animal node from General Tree habitat hierarchy."""
    for zone_node in map_root.children:
        zone_node.children = [
            child for child in zone_node.children 
            if not (f"(ID: #{target_id})" in child.node_name or f"(ID: {target_id})" in child.node_name)
        ]

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
    st.session_state.map_root.children = [TreeNode(z) for z in PHILIPPINE_ZONES]
    
    st.session_state.health_dll = DoublyLinkedList()
    st.session_state.triage_heap = MedicalPriorityQueueHeap()
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
        st.session_state.id_counter += 1

    # Seed Native Wildlife
    seed_initial("Agila", "Birds", "Mossy Cloud Mountain Forest", 2)
    seed_initial("Tami", "Mammals", "Lowland Dipterocarp Forest", 0)
    seed_initial("Pawikan", "Reptiles", "Mangrove & Coastal Wetland", 1)
    seed_initial("Kabag", "Mammals", "Karst Cave System", 3)
    seed_initial("Agila II", "Birds", "Mossy Cloud Mountain Forest", 2)

    st.session_state.triage_heap.push("Pilandok", "Mammals", "Lowland Dipterocarp Forest", 1, "Severe leg fracture / Emergency Triage")
    st.session_state.triage_heap.push("Bakawan", "Reptiles", "Mangrove & Coastal Wetland", 3, "Rescued from fish trap / Routine Intake")

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
            "⏳ Admission & Release Queue"
        ]
    )
    st.divider()
    st.caption(f"Registered Animals: {st.session_state.id_counter - 101}")
    st.caption(f"Active Eco-Zones: {len(PHILIPPINE_ZONES)}")

# Header Metrics
st.title("ANIMA Sanctuary Operations")
c1, c2, c3 = st.columns(3)
c1.metric("Active Animals", st.session_state.id_counter - 101, delta="BST Indexed")
c2.metric("Intake Queue", len(st.session_state.triage_heap.heap), delta="Priority Heap")
c3.metric("Next Registry ID", f"#{st.session_state.id_counter}", delta="Auto-Assigned")
st.divider()

# ==========================================================
# 6. MODULE 1: ANIMAL REGISTRY & MAP (WITH DELETION)
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
                
                st.session_state.id_counter += 1
                st.success(f"Registered {reg_name} (ID: #{aid})!")
                st.rerun()

        st.divider()
        
        # ANIMAL DELETION / DISCHARGE FEATURE
        st.markdown("### 🗑️ Delete / Discharge Animal Record")
        st.caption("Removes the animal node from both the BST Index and General Tree Habitat Hierarchy.")
        
        all_records_del = []
        in_order_bst(st.session_state.bst_root, all_records_del)
        
        if all_records_del:
            del_options = {
                f"#{a['Animal ID']} - {a['Name']} ({a['Species Class']}) [{a['Habitat Zone']}]": a['Animal ID'] 
                for a in all_records_del
            }
            target_del_label = st.selectbox("Select Animal to Delete:", list(del_options.keys()), key="del_select_box")
            target_del_id = del_options[target_del_label]
            
            if st.button("🚨 Delete Animal Record"):
                st.session_state.bst_root = delete_bst(st.session_state.bst_root, target_del_id)
                delete_from_general_tree(st.session_state.map_root, target_del_id)
                st.success(f"Successfully deleted Animal ID #{target_del_id} from Sanctuary Registry!")
                st.rerun()
        else:
            st.info("No animals available in registry for deletion.")

        st.divider()
        
        # SEARCH & MULTI-FILTER ENGINE
        st.markdown("### 🔍 Search & Multi-Filter Engine")
        
        all_records = []
        in_order_bst(st.session_state.bst_root, all_records)
        
        search_mode = st.radio("Search Method:", ["Numeric BST Search (O(log n))", "Name & Attribute Filter"], horizontal=True)
        
        if search_mode == "Numeric BST Search (O(log n))":
            search_target = st.number_input("Enter Animal ID", min_value=101, step=1)
            if st.button("Execute BST Search"):
                found_node, steps = bst_search(st.session_state.bst_root, int(search_target))
                if found_node:
                    st.success(f"Located in {steps} step(s): **{found_node.name}** ({found_node.species}) in *{found_node.zone}*")
                else:
                    st.error(f"Animal ID #{search_target} not found in BST index.")
        else:
            existing_names = sorted(list(set([r["Name"] for r in all_records])))
            filter_name = st.selectbox("Select/Type Animal Name:", ["-- All Names --"] + existing_names)
            filter_species = st.selectbox("Filter Species Class:", ["-- All Species --"] + SPECIES_CLASSES)
            filter_zone = st.selectbox("Filter Habitat Zone:", ["-- All Ecosystems --"] + PHILIPPINE_ZONES)
            
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
            
            sort_c1, sort_c2 = st.columns(2)
            with sort_c1:
                sort_key = st.selectbox("Sort Table By:", ["Animal ID (BST Traversal Order)", "Name", "Species Class", "Habitat Zone"])
            with sort_c2:
                sort_order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)
                
            reverse_flag = (sort_order == "Descending")
            
            if sort_key == "Animal ID (BST Traversal Order)":
                display_records = records if not reverse_flag else list(reversed(records))
            else:
                display_records = custom_bubble_sort(records, key=sort_key, reverse=reverse_flag)
                
            st.dataframe(display_records, use_container_width=True)
            
        with tab2:
            st.markdown("### 🌳 Habitat Zone Inspector")
            st.caption("Traverses the General Tree structure (`map_root.children`) to display habitat nodes in tabular form.")
            
            selected_zone_filter = st.selectbox(
                "Filter by Habitat Zone Node:", 
                ["-- All Habitat Zones (Full Tree) --"] + PHILIPPINE_ZONES
            )
            
            tree_table_rows = []
            for zone_node in st.session_state.map_root.children:
                if selected_zone_filter == "-- All Habitat Zones (Full Tree) --" or selected_zone_filter == zone_node.node_name:
                    for animal_node in zone_node.children:
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
# 7. MODULE 2: HEALTH LOG & MEDICAL HISTORY (DOUBLY LINKED LIST)
# ==========================================================

elif "Health Log" in selected_page:
    st.subheader("Animal Health Logs & Medical History (Doubly Linked List)")
    st.caption("Powered by a Doubly Linked List allowing forward and backward traversal through patient timelines.")
    
    all_animals = []
    in_order_bst(st.session_state.bst_root, all_animals)
    
    c_in, c_view = st.columns([1, 2])
    
    with c_in:
        st.markdown("### 📝 Add Medical Entry")
        
        if not all_animals:
            st.warning("No animals registered in the sanctuary yet. Please register or admit an animal first.")
        else:
            st.markdown("#### 🔍 Patient Lookup & Selection")
            
            add_search_mode = st.radio(
                "Find Patient By:",
                ["Name Autocomplete & Species Filter", "Numeric ID Search"],
                horizontal=True,
                key="add_med_search_mode"
            )
            
            selected_target_id = None
            selected_animal_info = None
            
            if add_search_mode == "Name Autocomplete & Species Filter":
                med_spec_filter = st.selectbox(
                    "Filter Species Class:", 
                    ["-- All Species --"] + SPECIES_CLASSES, 
                    key="add_med_spec_filter"
                )
                
                filtered_patients = all_animals
                if med_spec_filter != "-- All Species --":
                    filtered_patients = [a for a in filtered_patients if a["Species Class"] == med_spec_filter]
                
                if filtered_patients:
                    patient_options = {
                        f"#{a['Animal ID']} - {a['Name']} ({a['Species Class']}) [{a['Habitat Zone']}]": a 
                        for a in filtered_patients
                    }
                    chosen_patient_label = st.selectbox(
                        "Type / Select Target Patient:", 
                        list(patient_options.keys()), 
                        key="add_med_patient_choice"
                    )
                    selected_animal_info = patient_options[chosen_patient_label]
                    selected_target_id = selected_animal_info["Animal ID"]
                else:
                    st.warning("No animal records match the selected species filter.")
            else:
                query_id_input = st.number_input("Enter Animal ID:", min_value=101, step=1, key="add_med_id_input")
                selected_target_id = int(query_id_input)
                selected_animal_info = next((a for a in all_animals if a["Animal ID"] == selected_target_id), None)
            
            if selected_animal_info:
                st.info(
                    f"🎯 **Target Patient:** {selected_animal_info['Name']} (ID: #{selected_target_id})\n\n"
                    f"• Class: **{selected_animal_info['Species Class']}** | Habitat: **{selected_animal_info['Habitat Zone']}**"
                )
            elif selected_target_id:
                st.caption(f"Target Patient ID: #{selected_target_id} (Unindexed)")

            st.markdown("#### 📋 Log New Treatment Node")
            with st.form("med_form", clear_on_submit=True):
                diagnosis = st.text_input("Diagnosis / Condition Note")
                treatment = st.text_area("Treatment / Medication Administered")
                submit_med = st.form_submit_button("Append Entry to Doubly Linked List")
                
                if submit_med:
                    if not selected_target_id:
                        st.error("Please select a valid animal before submitting.")
                    elif not diagnosis or not treatment:
                        st.error("Please provide both a diagnosis and treatment description.")
                    else:
                        st.session_state.health_dll.append(selected_target_id, diagnosis, treatment)
                        patient_name = selected_animal_info['Name'] if selected_animal_info else f"ID #{selected_target_id}"
                        st.success(f"Medical entry logged for {patient_name}!")
                        st.rerun()

    with c_view:
        st.markdown("### 🔬 Patient Medical Timeline (DLL View)")
        
        if selected_target_id:
            patient_history = st.session_state.health_dll.get_patient_history(selected_target_id)
            
            if selected_animal_info:
                st.markdown(f"#### Active Timeline: **{selected_animal_info['Name']}** (ID: #{selected_target_id})")
                st.caption(f"Species Class: **{selected_animal_info['Species Class']}** | Ecosystem: **{selected_animal_info['Habitat Zone']}**")
            else:
                st.markdown(f"#### Active Timeline for Animal ID: #{selected_target_id}")
                
            if patient_history:
                st.dataframe(patient_history, use_container_width=True)
            else:
                st.info(f"No medical treatment entries logged for ID #{selected_target_id} yet.")
        else:
            st.info("Select or search for an animal on the left panel to display its medical history.")

# ==========================================================
# 8. MODULE 3: UNIFIED ADMISSION & SYSTEM ADMIT INTEGRATION
# ==========================================================

elif "Admission" in selected_page:
    st.subheader("Sanctuary Admission & Emergency Triage Pipeline")
    st.caption("A unified intake engine powered by a Priority Heap with automatic cross-module admission indexing.")
    
    col_intake, col_queue_view = st.columns([1, 2])
    
    with col_intake:
        st.markdown("### 📥 Animal Intake & Triage Registration")
        with st.form("unified_intake_form", clear_on_submit=True):
            intake_name = st.text_input("Animal / Rescue Name")
            intake_species = st.selectbox("Species Class", SPECIES_CLASSES)
            intake_zone = st.selectbox("Target Philippine Ecosystem Zone", PHILIPPINE_ZONES)
            intake_priority = st.selectbox(
                "Triage Priority Level:",
                [1, 2, 3],
                format_func=lambda x: f"Priority {x} - {'🚨 Critical Emergency (Immediate Care)' if x==1 else '⚠️ Urgent Care Required' if x==2 else '⏳ Routine Sanctuary Intake (FIFO)'}"
            )
            intake_reason = st.text_area("Intake Reason / Medical Condition")
            
            submit_intake = st.form_submit_button("Enqueue Animal for Admission")
            
            if submit_intake:
                if not intake_name or not intake_reason:
                    st.error("Please fill in both the animal name and intake reason.")
                else:
                    st.session_state.triage_heap.push(
                        intake_name, 
                        intake_species, 
                        intake_zone,
                        intake_priority, 
                        intake_reason
                    )
                    st.success(f"Successfully enqueued **{intake_name}** into Triage Pipeline!")
                    st.rerun()

    with col_queue_view:
        st.markdown("### 📋 Live Triage Processing Queue")
        st.caption("Sorted automatically: Critical emergencies first, followed by routine arrivals in order of intake.")
        
        sorted_pipeline = st.session_state.triage_heap.get_sorted_list()
        
        if sorted_pipeline:
            display_queue = []
            for item in sorted_pipeline:
                p_level = item["Priority Level"]
                p_tag = "🚨 Priority 1 - Critical" if p_level == 1 else "⚠️ Priority 2 - Urgent" if p_level == 2 else "⏳ Priority 3 - Routine"
                
                display_queue.append({
                    "Triage Status": p_tag,
                    "Animal Name": item["Name"],
                    "Species": item["Species"],
                    "Target Ecosystem": item["Zone"],
                    "Condition / Reason": item["Condition"]
                })
            
            st.dataframe(display_queue, use_container_width=True)
            
            st.divider()
            if st.button("🩺 Process & Admit Next Animal to Global System"):
                # Pop next animal from Heap
                next_patient = st.session_state.triage_heap.pop()
                aid = st.session_state.id_counter
                
                # 1. Insert into BST Index
                new_bst = BSTNode(aid, next_patient['Name'], next_patient['Species'], next_patient['Zone'])
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
                
                # 2. Insert into General Tree Habitat Hierarchy
                zone_idx = PHILIPPINE_ZONES.index(next_patient['Zone'])
                st.session_state.map_root.children[zone_idx].children.append(
                    TreeNode(f"{next_patient['Name']} (ID: #{aid})")
                )
                
                # 3. Create Initial Medical Log in Doubly Linked List
                st.session_state.health_dll.append(
                    aid, 
                    f"Admitted from Intake Queue: {next_patient['Condition']}", 
                    "Assigned sanctuary housing and passed medical evaluation."
                )
                
                st.session_state.id_counter += 1
                st.success(
                    f"Admitted **{next_patient['Name']}** into **{next_patient['Zone']}**! "
                    f"Assigned Animal ID: **#{aid}** (Added to Global Registry & Health Log)."
                )
                st.rerun()
        else:
            st.info("The sanctuary intake pipeline is currently empty. All incoming animals have been processed!")