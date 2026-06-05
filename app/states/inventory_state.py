import reflex as rx
from typing import TypedDict


class Item(TypedDict):
    id: str
    sku: str
    legacy_code: str
    code: str
    name: str
    description: str
    category: str
    unit: str
    on_hand: float
    reserved: float
    available: float
    incoming: float
    min_level: float
    max_level: float
    reorder_point: float
    safety_stock: float
    total_received: float
    total_issued: float
    last_received_date: str
    last_issued_date: str
    location: str
    status: str
    is_napza: bool
    is_hazard: bool
    vendor: str
    last_updated: str
    created_at: str


class Lot(TypedDict):
    id: str
    item_id: str
    item_name: str
    lot_number: str
    quantity: float
    unit: str
    received_date: str
    expiry_date: str
    status: str
    location: str
    vendor: str
    days_to_expiry: int


class InventoryState(rx.State):
    items: list[Item] = [
        {
            "id": "ITM-001",
            "sku": "RGT-MTH-001",
            "legacy_code": "QC-MTH-OLD-01",
            "code": "RGT-MTH-001",
            "name": "Methanol HPLC Grade",
            "description": "HPLC-grade methanol for chromatographic analysis",
            "category": "Solvent",
            "unit": "L",
            "on_hand": 45.5,
            "reserved": 5.0,
            "available": 40.5,
            "incoming": 25.0,
            "min_level": 20.0,
            "max_level": 100.0,
            "reorder_point": 25.0,
            "safety_stock": 10.0,
            "total_received": 120.0,
            "total_issued": 74.5,
            "last_received_date": "2024-10-15",
            "last_issued_date": "2024-11-12",
            "location": "Solvent Cabinet A",
            "status": "Released",
            "is_napza": False,
            "is_hazard": True,
            "vendor": "Merck KGaA",
            "last_updated": "2024-11-12",
            "created_at": "2023-04-12",
        },
        {
            "id": "ITM-002",
            "sku": "RGT-ACE-002",
            "legacy_code": "QC-ACE-OLD-02",
            "code": "RGT-ACE-002",
            "name": "Acetonitrile HPLC Grade",
            "description": "HPLC-grade acetonitrile for mobile phase preparation",
            "category": "Solvent",
            "unit": "L",
            "on_hand": 12.0,
            "reserved": 3.0,
            "available": 9.0,
            "incoming": 0.0,
            "min_level": 15.0,
            "max_level": 80.0,
            "reorder_point": 18.0,
            "safety_stock": 8.0,
            "total_received": 60.0,
            "total_issued": 48.0,
            "last_received_date": "2024-09-20",
            "last_issued_date": "2024-11-10",
            "location": "Solvent Cabinet A",
            "status": "Released",
            "is_napza": False,
            "is_hazard": True,
            "vendor": "Sigma-Aldrich",
            "last_updated": "2024-11-10",
            "created_at": "2023-04-12",
        },
        {
            "id": "ITM-003",
            "sku": "STD-PAR-003",
            "legacy_code": "QC-PAR-OLD-03",
            "code": "STD-PAR-003",
            "name": "Paracetamol Reference Standard",
            "description": "USP reference standard for paracetamol assay",
            "category": "Reference Standard",
            "unit": "g",
            "on_hand": 5.250,
            "reserved": 0.5,
            "available": 4.750,
            "incoming": 0.0,
            "min_level": 2.0,
            "max_level": 10.0,
            "reorder_point": 3.0,
            "safety_stock": 1.5,
            "total_received": 8.0,
            "total_issued": 2.75,
            "last_received_date": "2024-05-15",
            "last_issued_date": "2024-11-11",
            "location": "Cold Storage R-1",
            "status": "Released",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "USP",
            "last_updated": "2024-11-11",
            "created_at": "2023-06-01",
        },
        {
            "id": "ITM-004",
            "sku": "NPZ-MOR-004",
            "legacy_code": "QC-MOR-OLD-04",
            "code": "NPZ-MOR-004",
            "name": "Morphine Sulfate Standard",
            "description": "Controlled NAPZA reference standard, restricted access",
            "category": "Controlled Substance",
            "unit": "mg",
            "on_hand": 250.0,
            "reserved": 50.0,
            "available": 200.0,
            "incoming": 0.0,
            "min_level": 100.0,
            "max_level": 500.0,
            "reorder_point": 150.0,
            "safety_stock": 80.0,
            "total_received": 500.0,
            "total_issued": 250.0,
            "last_received_date": "2024-02-10",
            "last_issued_date": "2024-11-09",
            "location": "Vault NPZ-01",
            "status": "Released",
            "is_napza": True,
            "is_hazard": True,
            "vendor": "USP",
            "last_updated": "2024-11-09",
            "created_at": "2023-01-15",
        },
        {
            "id": "ITM-005",
            "sku": "RGT-PHB-005",
            "legacy_code": "QC-PHB-OLD-05",
            "code": "RGT-PHB-005",
            "name": "Phosphate Buffer pH 6.8",
            "description": "Internally prepared phosphate buffer solution",
            "category": "Buffer",
            "unit": "L",
            "on_hand": 8.0,
            "reserved": 0.0,
            "available": 8.0,
            "incoming": 0.0,
            "min_level": 10.0,
            "max_level": 50.0,
            "reorder_point": 12.0,
            "safety_stock": 5.0,
            "total_received": 20.0,
            "total_issued": 12.0,
            "last_received_date": "2024-11-01",
            "last_issued_date": "2024-11-08",
            "location": "Buffer Shelf B",
            "status": "Released",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "Internal Prep",
            "last_updated": "2024-11-08",
            "created_at": "2023-08-10",
        },
        {
            "id": "ITM-006",
            "sku": "GLW-VOL-006",
            "legacy_code": "QC-VOL-OLD-06",
            "code": "GLW-VOL-006",
            "name": "Volumetric Flask 100mL Class A",
            "description": "Class A volumetric flask, certified",
            "category": "Glassware",
            "unit": "pcs",
            "on_hand": 24.0,
            "reserved": 0.0,
            "available": 24.0,
            "incoming": 0.0,
            "min_level": 10.0,
            "max_level": 50.0,
            "reorder_point": 15.0,
            "safety_stock": 5.0,
            "total_received": 30.0,
            "total_issued": 6.0,
            "last_received_date": "2024-04-20",
            "last_issued_date": "2024-11-05",
            "location": "Glassware Cabinet C",
            "status": "Released",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "Pyrex",
            "last_updated": "2024-11-05",
            "created_at": "2022-11-10",
        },
        {
            "id": "ITM-007",
            "sku": "STD-CAF-007",
            "legacy_code": "QC-CAF-OLD-07",
            "code": "STD-CAF-007",
            "name": "Caffeine Reference Standard",
            "description": "USP caffeine reference standard",
            "category": "Reference Standard",
            "unit": "g",
            "on_hand": 0.0,
            "reserved": 0.0,
            "available": 0.0,
            "incoming": 2.0,
            "min_level": 1.0,
            "max_level": 5.0,
            "reorder_point": 1.5,
            "safety_stock": 0.5,
            "total_received": 4.0,
            "total_issued": 4.0,
            "last_received_date": "2024-03-12",
            "last_issued_date": "2024-11-01",
            "location": "Cold Storage R-1",
            "status": "Out of Stock",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "USP",
            "last_updated": "2024-11-01",
            "created_at": "2023-02-08",
        },
        {
            "id": "ITM-008",
            "sku": "RGT-NAOH-008",
            "legacy_code": "QC-NAOH-OLD-08",
            "code": "RGT-NAOH-008",
            "name": "Sodium Hydroxide 0.1N",
            "description": "Standardized 0.1N sodium hydroxide titrant",
            "category": "Reagent",
            "unit": "L",
            "on_hand": 15.0,
            "reserved": 2.0,
            "available": 13.0,
            "incoming": 0.0,
            "min_level": 5.0,
            "max_level": 30.0,
            "reorder_point": 8.0,
            "safety_stock": 3.0,
            "total_received": 25.0,
            "total_issued": 10.0,
            "last_received_date": "2024-11-05",
            "last_issued_date": "2024-11-12",
            "location": "Reagent Shelf D",
            "status": "Released",
            "is_napza": False,
            "is_hazard": True,
            "vendor": "Internal Prep",
            "last_updated": "2024-11-12",
            "created_at": "2023-05-22",
        },
        {
            "id": "ITM-009",
            "sku": "STD-IBU-009",
            "legacy_code": "QC-IBU-OLD-09",
            "code": "STD-IBU-009",
            "name": "Ibuprofen Working Standard",
            "description": "Internal working standard, awaiting QC release",
            "category": "Reference Standard",
            "unit": "g",
            "on_hand": 2.100,
            "reserved": 0.0,
            "available": 2.100,
            "incoming": 0.0,
            "min_level": 1.0,
            "max_level": 5.0,
            "reorder_point": 1.5,
            "safety_stock": 0.5,
            "total_received": 2.1,
            "total_issued": 0.0,
            "last_received_date": "2024-11-13",
            "last_issued_date": "",
            "location": "Cold Storage R-1",
            "status": "Pending Release",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "Sigma-Aldrich",
            "last_updated": "2024-11-13",
            "created_at": "2024-11-13",
        },
        {
            "id": "ITM-010",
            "sku": "CON-FIL-010",
            "legacy_code": "QC-FIL-OLD-10",
            "code": "CON-FIL-010",
            "name": "PTFE Syringe Filter 0.45μm",
            "description": "Disposable PTFE syringe filter for sample preparation",
            "category": "Consumable",
            "unit": "pcs",
            "on_hand": 480.0,
            "reserved": 50.0,
            "available": 430.0,
            "incoming": 0.0,
            "min_level": 100.0,
            "max_level": 1000.0,
            "reorder_point": 200.0,
            "safety_stock": 75.0,
            "total_received": 600.0,
            "total_issued": 120.0,
            "last_received_date": "2024-10-07",
            "last_issued_date": "2024-11-07",
            "location": "Consumable Shelf E",
            "status": "Released",
            "is_napza": False,
            "is_hazard": False,
            "vendor": "Millipore",
            "last_updated": "2024-11-07",
            "created_at": "2022-09-10",
        },
    ]

    lots: list[Lot] = [
        {
            "id": "LOT-001",
            "item_id": "ITM-001",
            "item_name": "Methanol HPLC Grade",
            "lot_number": "MTH240801-A",
            "quantity": 25.0,
            "unit": "L",
            "received_date": "2024-08-01",
            "expiry_date": "2026-08-01",
            "status": "Released",
            "location": "Solvent Cabinet A",
            "vendor": "Merck KGaA",
            "days_to_expiry": 620,
        },
        {
            "id": "LOT-002",
            "item_id": "ITM-001",
            "item_name": "Methanol HPLC Grade",
            "lot_number": "MTH241015-B",
            "quantity": 20.5,
            "unit": "L",
            "received_date": "2024-10-15",
            "expiry_date": "2026-10-15",
            "status": "Released",
            "location": "Solvent Cabinet A",
            "vendor": "Merck KGaA",
            "days_to_expiry": 695,
        },
        {
            "id": "LOT-003",
            "item_id": "ITM-002",
            "item_name": "Acetonitrile HPLC Grade",
            "lot_number": "ACE240920-A",
            "quantity": 12.0,
            "unit": "L",
            "received_date": "2024-09-20",
            "expiry_date": "2025-03-20",
            "status": "Released",
            "location": "Solvent Cabinet A",
            "vendor": "Sigma-Aldrich",
            "days_to_expiry": 122,
        },
        {
            "id": "LOT-004",
            "item_id": "ITM-003",
            "item_name": "Paracetamol Reference Standard",
            "lot_number": "PAR-USP-2024-05",
            "quantity": 5.250,
            "unit": "g",
            "received_date": "2024-05-15",
            "expiry_date": "2025-05-15",
            "status": "Released",
            "location": "Cold Storage R-1",
            "vendor": "USP",
            "days_to_expiry": 178,
        },
        {
            "id": "LOT-005",
            "item_id": "ITM-004",
            "item_name": "Morphine Sulfate Standard",
            "lot_number": "MOR-USP-2024-02",
            "quantity": 250.0,
            "unit": "mg",
            "received_date": "2024-02-10",
            "expiry_date": "2025-02-10",
            "status": "Released",
            "location": "Vault NPZ-01",
            "vendor": "USP",
            "days_to_expiry": 84,
        },
        {
            "id": "LOT-006",
            "item_id": "ITM-005",
            "item_name": "Phosphate Buffer pH 6.8",
            "lot_number": "PHB-INT-241101",
            "quantity": 8.0,
            "unit": "L",
            "received_date": "2024-11-01",
            "expiry_date": "2024-12-01",
            "status": "Released",
            "location": "Buffer Shelf B",
            "vendor": "Internal Prep",
            "days_to_expiry": 13,
        },
        {
            "id": "LOT-007",
            "item_id": "ITM-008",
            "item_name": "Sodium Hydroxide 0.1N",
            "lot_number": "NAOH-INT-241105",
            "quantity": 15.0,
            "unit": "L",
            "received_date": "2024-11-05",
            "expiry_date": "2025-02-05",
            "status": "Released",
            "location": "Reagent Shelf D",
            "vendor": "Internal Prep",
            "days_to_expiry": 79,
        },
        {
            "id": "LOT-008",
            "item_id": "ITM-009",
            "item_name": "Ibuprofen Working Standard",
            "lot_number": "IBU-SIG-241113",
            "quantity": 2.100,
            "unit": "g",
            "received_date": "2024-11-13",
            "expiry_date": "2025-11-13",
            "status": "Pending Release",
            "location": "Cold Storage R-1",
            "vendor": "Sigma-Aldrich",
            "days_to_expiry": 360,
        },
        {
            "id": "LOT-009",
            "item_id": "ITM-010",
            "item_name": "PTFE Syringe Filter 0.45μm",
            "lot_number": "FIL-MIL-241007",
            "quantity": 480.0,
            "unit": "pcs",
            "received_date": "2024-10-07",
            "expiry_date": "2027-10-07",
            "status": "Released",
            "location": "Consumable Shelf E",
            "vendor": "Millipore",
            "days_to_expiry": 1050,
        },
    ]

    search_query: str = ""
    category_filter: str = "All"
    status_filter: str = "All"
    selected_item_id: str = ""

    @rx.var
    def categories(self) -> list[str]:
        cats = ["All"]
        seen = set()
        for item in self.items:
            if item["category"] not in seen:
                seen.add(item["category"])
                cats.append(item["category"])
        return cats

    @rx.var
    def statuses(self) -> list[str]:
        return [
            "All",
            "Released",
            "Pending Release",
            "Quarantine",
            "Out of Stock",
        ]

    @rx.var
    def filtered_items(self) -> list[Item]:
        result = self.items
        q = self.search_query.lower().strip()
        if q:
            result = [
                i
                for i in result
                if q in i["name"].lower()
                or q in i["sku"].lower()
                or q in i["legacy_code"].lower()
                or q in i["category"].lower()
                or q in i["description"].lower()
            ]
        if self.category_filter != "All":
            result = [
                i for i in result if i["category"] == self.category_filter
            ]
        if self.status_filter != "All":
            result = [i for i in result if i["status"] == self.status_filter]
        return result

    @rx.var
    def total_items(self) -> int:
        return len(self.items)

    @rx.var
    def low_stock_count(self) -> int:
        return len([i for i in self.items if i["on_hand"] < i["min_level"]])

    @rx.var
    def out_of_stock_count(self) -> int:
        return len([i for i in self.items if i["on_hand"] <= 0])

    @rx.var
    def expiring_soon_count(self) -> int:
        return len(
            [
                l
                for l in self.lots
                if l["days_to_expiry"] <= 90 and l["days_to_expiry"] >= 0
            ]
        )

    @rx.var
    def napza_count(self) -> int:
        return len([i for i in self.items if i["is_napza"]])

    @rx.var
    def total_lots(self) -> int:
        return len(self.lots)

    @rx.var
    def selected_item(self) -> Item:
        for i in self.items:
            if i["id"] == self.selected_item_id:
                return i
        return (
            self.items[0]
            if self.items
            else {
                "id": "",
                "sku": "",
                "legacy_code": "",
                "code": "",
                "name": "",
                "description": "",
                "category": "",
                "unit": "",
                "on_hand": 0.0,
                "reserved": 0.0,
                "available": 0.0,
                "incoming": 0.0,
                "min_level": 0.0,
                "max_level": 0.0,
                "reorder_point": 0.0,
                "safety_stock": 0.0,
                "total_received": 0.0,
                "total_issued": 0.0,
                "last_received_date": "",
                "last_issued_date": "",
                "location": "",
                "status": "",
                "is_napza": False,
                "is_hazard": False,
                "vendor": "",
                "last_updated": "",
                "created_at": "",
            }
        )

    @rx.var
    def selected_item_lots(self) -> list[Lot]:
        return [l for l in self.lots if l["item_id"] == self.selected_item_id]

    @rx.event
    def set_search(self, q: str):
        self.search_query = q

    @rx.event
    def set_category(self, c: str):
        self.category_filter = c

    @rx.event
    def set_status(self, s: str):
        self.status_filter = s

    @rx.event
    def select_item(self, item_id: str):
        self.selected_item_id = item_id
        return rx.redirect(f"/inventory/{item_id}")

    @rx.event
    def load_item_from_route(self):
        item_id = self.router.page.params.get("item_id", "")
        if item_id:
            self.selected_item_id = item_id

    def _validate_stock_change(
        self, item_id: str, delta: float
    ) -> tuple[bool, str]:
        """Service-layer rule: reject negative stock without silent clamping."""
        for i in self.items:
            if i["id"] == item_id:
                new_qty = i["on_hand"] + delta
                if new_qty < 0:
                    return (
                        False,
                        f"Operation rejected: would result in negative stock ({new_qty:.3f} {i['unit']}). Stock cannot go below zero.",
                    )
                return (True, "OK")
        return (False, f"Item {item_id} not found.")