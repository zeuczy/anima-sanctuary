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
# 2. CONSTANTS & BOUNDS
# ==========================================================

PHILIPPINE_ZONES = [
    "Lowland Dipterocarp Forest",
    "Mangrove & Coastal Wetland",
    "Mossy Cloud Mountain Forest",
    "Karst Cave System"
]

ZONE_CAPACITIES = {
    "Lowland Dipterocarp Forest": 5,
    "Mangrove & Coastal Wetland": 4,
    "Mossy Cloud Mountain Forest": 3,
    "Karst Cave System": 4
}

SPECIES_CLASSES = [
    "Mammals",
    "Birds",
    "Reptiles",
    "Amphibians",
    "Fish",
    "Invertebrates"
]

STATUS_TAGS = [
    "🟢 Cleared / Healthy",
    "🟡 Under Observation",
    "🔴 Critical Medical Hold"
]

# ==========================================================
# 3. DSA CLASSES (BST, GENERAL TREE, DLL, HEAP, ARCHIVE DLL)
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
    def __init__(self, animal_id, timestamp, diagnosis, treatment, status_tag="🟢 Cleared / Healthy"):
        self.animal_id = animal_id
        self.timestamp = timestamp
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.status_tag = status_tag
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, animal_id, diagnosis, treatment, status_tag="🟢 Cleared / Healthy"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_node = DLLNode(animal_id, timestamp, diagnosis, treatment, status_tag)
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
                    "Status Tag": curr.status_tag,
                    "Diagnosis": curr.diagnosis,
                    "Treatment": curr.treatment
                })
            curr = curr.next
        return records

class ArchiveDLLNode:
    def __init__(self, animal_id, name, species, zone, release_date, release_notes):
        self.animal_id = animal_id
        self.name = name
        self.species = species
        self.zone = zone
        self.release_date = release_date
        self.release_notes = release_notes
        self.prev = None
        self.next = None

class ArchiveDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, animal_id, name, species, zone, release_notes):
        release_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_node = ArchiveDLLNode(animal_id, name, species, zone, release_date, release_notes)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def get_all_archived(self):
        records = []
        curr = self.head
        while curr:
            records.append({
                "Animal ID": f"#{curr.animal_id}",
                "Name": curr.name,
                "Species Class": curr.species,
                "Former Habitat": curr.zone,
                "Release Timestamp": curr.release_date,
                "Release Outcome Notes": curr.release_notes
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

    def peek(self):
        return sorted(self.heap)[0][2] if self.heap else None

    def get_sorted_list(self):
        return [item[2] for item in sorted(self.heap)]

# ==========================================================
# 4. ALGORITHMS & TREE UTILITIES
# ==========================================================

def get_zone_occupancy(map_root, zone_name):
    """Calculates current number of animals in a specific General Tree Habitat node."""
    for zone_node in map_root.children:
        if zone_node.node_name == zone_name:
            return len(zone_node.children)
    return 0

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
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_bst(root, target_id):
    """Recursive Binary Search Tree Deletion Algorithm."""
    if root is None:
        return root
    if target_id < root.animal_id:
        root.left = delete_bst(root.left, target_id)
    elif target_id > root.animal_id:
        root.right = delete_bst(root.right, target_id)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
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
# 5. INITIALIZATION & SESSION STATE
# ==========================================================

if "initialized" not in st.session_state:
    st.session_state.bst_root = None
    st.session_state.map_root = TreeNode("ANIMA Sanctuary (Philippines)")
    st.session_state.map_root.children = [TreeNode(z) for z in PHILIPPINE_ZONES]
    
    st.session_state.health_dll = DoublyLinkedList()
    st.session_state.archive_dll = ArchiveDoublyLinkedList()
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
        st.session_state.health_dll.append(aid, "Intake Evaluation", "Passed physical evaluation.", "🟢 Cleared / Healthy")
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
# 6. SIDEBAR NAVIGATION
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
    st.caption(f"Active Registered Animals: {st.session_state.id_counter - 101}")
    st.caption(f"Archived Releases: {len(st.session_state.archive_dll.get_all_archived())}")
    st.caption(f"Active Eco-Zones: {len(PHILIPPINE_ZONES)}")

# Header Metrics
st.title("ANIMA Sanctuary Operations")
c1, c2, c3 = st.columns(3)
c1.metric("Active Animals", st.session_state.id_counter - 101, delta="BST Indexed")
c2.metric("Intake Queue", len(st.session_state.triage_heap.heap), delta="Priority Heap")
c3.metric("Next Registry ID", f"#{st.session_state.id_counter}", delta="Auto-Assigned")
st.divider()

# ==========================================================
# 7. MODULE 1: ANIMAL REGISTRY & MAP
# ==========================================================

if "Animal Registry" in selected_page:
    st.subheader("Sanctuary Animal Registry & Physical Map")
    
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.markdown("### ➕ Register New Animal")
        with st.form("add_animal_form", clear_on_submit=True):
            reg_name = st.text_input("Animal Name (e.g., Agila, Pawikan)")
            reg_species = st.selectbox("Species Class", SPECIES_CLASSES)
            reg_zone = st.selectbox(
                "Philippine Ecosystem Zone", 
                PHILIPPINE_ZONES,
                format_func=lambda z: f"{z} (Occ: {get_zone_occupancy(st.session_state.map_root, z)}/{ZONE_CAPACITIES[z]})"
            )
            submit_reg = st.form_submit_button("Complete Registration")
            
            if submit_reg and reg_name:
                current_occ = get_zone_occupancy(st.session_state.map_root, reg_zone)
                max_cap = ZONE_CAPACITIES[reg_zone]
                
                if current_occ >= max_cap:
                    st.error(f"⛔ **Habitat Overflow Error:** '{reg_zone}' has reached maximum capacity ({current_occ}/{max_cap}). Please select another ecosystem zone.")
                else:
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
                    st.session_state.health_dll.append(aid, "Intake Checkup", "Newly registered record created.", "🟢 Cleared / Healthy")
                    
                    st.session_state.id_counter += 1
                    st.success(f"Registered {reg_name} (ID: #{aid}) into {reg_zone}!")
                    st.rerun()

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
        tab1, tab2, tab3 = st.tabs(["📋 Global Registry Index", "🌳 Habitat Inspector & Capacities", "🌿 Released Archives (Archive DLL)"])
        
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
            
            # RELOCATED DISCHARGE & RELEASE / DELETE MODULE (Positioned below Global Registry Index)
            st.divider()
            st.markdown("### 🌿 Discharge & Release / Delete Animal")
            st.caption("Release animals back to the wild (archiving history) or perform permanent record deletion.")
            
            all_records_del = []
            in_order_bst(st.session_state.bst_root, all_records_del)
            
            if all_records_del:
                del_options = {
                    f"#{a['Animal ID']} - {a['Name']} ({a['Species Class']}) [{a['Habitat Zone']}]": a 
                    for a in all_records_del
                }
                target_del_label = st.selectbox("Select Target Animal:", list(del_options.keys()), key="del_select_box")
                target_animal = del_options[target_del_label]
                target_del_id = target_animal["Animal ID"]
                
                action_type = st.radio("Action Type:", ["🌿 Release to Wild (Archive Node)", "🚨 Permanent Deletion"], horizontal=True)
                release_note = st.text_input("Outcome / Release Notes", value="Successfully rehabilitated and released to natural habitat.")
                
                if st.button("Execute Record Action"):
                    if action_type == "🌿 Release to Wild (Archive Node)":
                        st.session_state.archive_dll.append(
                            target_animal["Animal ID"],
                            target_animal["Name"],
                            target_animal["Species Class"],
                            target_animal["Habitat Zone"],
                            release_note
                        )
                        st.success(f"Archived and Released **{target_animal['Name']}** (ID: #{target_del_id}) to the wild!")
                    else:
                        st.warning(f"Permanently deleted Animal ID #{target_del_id}.")
                    
                    st.session_state.bst_root = delete_bst(st.session_state.bst_root, target_del_id)
                    delete_from_general_tree(st.session_state.map_root, target_del_id)
                    st.rerun()
            else:
                st.info("No animals available in registry for discharge.")
            
        with tab2:
            st.markdown("### 🌳 Ecosystem Zone Capacity & Node Hierarchy")
            
            cap_cols = st.columns(4)
            for i, zone in enumerate(PHILIPPINE_ZONES):
                occ = get_zone_occupancy(st.session_state.map_root, zone)
                cap = ZONE_CAPACITIES[zone]
                cap_cols[i].metric(zone.split(" ")[0], f"{occ} / {cap}", delta="Full" if occ>=cap else f"{cap-occ} spots left")
            
            st.divider()
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

        with tab3:
            st.markdown("### 🌿 Released & Archived Wildlife Directory")
            st.caption("Powered by an Archive Doubly Linked List storing historical records of rehabilitated animals.")
            
            archived_list = st.session_state.archive_dll.get_all_archived()
            if archived_list:
                st.dataframe(archived_list, use_container_width=True)
            else:
                st.info("No animals have been released/archived yet.")

# ==========================================================
# 8. MODULE 2: HEALTH LOG & MEDICAL HISTORY
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
                status_tag = st.selectbox("Medical Status Badge:", STATUS_TAGS)
                diagnosis = st.text_input("Diagnosis / Condition Note")
                treatment = st.text_area("Treatment / Medication Administered")
                submit_med = st.form_submit_button("Append Entry to Doubly Linked List")
                
                if submit_med:
                    if not selected_target_id:
                        st.error("Please select a valid animal before submitting.")
                    elif not diagnosis or not treatment:
                        st.error("Please provide both a diagnosis and treatment description.")
                    else:
                        st.session_state.health_dll.append(selected_target_id, diagnosis, treatment, status_tag)
                        patient_name = selected_animal_info['Name'] if selected_animal_info else f"ID #{selected_target_id}"
                        st.success(f"Medical entry logged for {patient_name} [{status_tag}]!")
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
# 9. MODULE 3: UNIFIED ADMISSION & CAPACITY-CHECKED ADMIT
# ==========================================================

elif "Admission" in selected_page:
    st.subheader("Sanctuary Admission & Emergency Triage Pipeline")
    st.caption("A unified intake engine powered by a Priority Heap with ecosystem capacity enforcement.")
    
    col_intake, col_queue_view = st.columns([1, 2])
    
    with col_intake:
        st.markdown("### 📥 Animal Intake & Triage Registration")
        with st.form("unified_intake_form", clear_on_submit=True):
            intake_name = st.text_input("Animal / Rescue Name")
            intake_species = st.selectbox("Species Class", SPECIES_CLASSES)
            intake_zone = st.selectbox(
                "Target Philippine Ecosystem Zone", 
                PHILIPPINE_ZONES,
                format_func=lambda z: f"{z} (Occ: {get_zone_occupancy(st.session_state.map_root, z)}/{ZONE_CAPACITIES[z]})"
            )
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
            
            next_candidate = st.session_state.triage_heap.peek()
            
            if next_candidate:
                target_z = next_candidate['Zone']
                current_occ = get_zone_occupancy(st.session_state.map_root, target_z)
                max_cap = ZONE_CAPACITIES[target_z]
                
                if current_occ >= max_cap:
                    st.error(
                        f"⛔ **Admission Blocked:** Next candidate **{next_candidate['Name']}** cannot be admitted. "
                        f"Target habitat **'{target_z}'** is at full capacity ({current_occ}/{max_cap}). "
                        f"Please release/discharge an animal from '{target_z}' first."
                    )
                else:
                    if st.button(f"🩺 Process & Admit Next Animal ({next_candidate['Name']}) to Global System"):
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
                        
                        # 2. Insert into General Tree Hierarchy
                        zone_idx = PHILIPPINE_ZONES.index(next_patient['Zone'])
                        st.session_state.map_root.children[zone_idx].children.append(
                            TreeNode(f"{next_patient['Name']} (ID: #{aid})")
                        )
                        
                        # 3. Initial Health Log with Status Badge mapping
                        auto_status_tag = (
                            "🔴 Critical Medical Hold" if next_patient['Priority Level'] == 1 
                            else "🟡 Under Observation" if next_patient['Priority Level'] == 2 
                            else "🟢 Cleared / Healthy"
                        )
                        st.session_state.health_dll.append(
                            aid, 
                            f"Admitted from Triage: {next_patient['Condition']}", 
                            "Assigned housing and started care plan.",
                            auto_status_tag
                        )
                        
                        st.session_state.id_counter += 1
                        st.success(
                            f"Admitted **{next_patient['Name']}** into **{next_patient['Zone']}**! "
                            f"Assigned ID: **#{aid}** [{auto_status_tag}]."
                        )
                        st.rerun()
        else:
            st.info("The sanctuary intake pipeline is currently empty. All incoming animals have been processed!")
