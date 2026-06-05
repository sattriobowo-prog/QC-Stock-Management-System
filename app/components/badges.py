import reflex as rx


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.match(
            status,
            ("Released", rx.icon("circle_check", class_name="h-3 w-3")),
            ("Pending Release", rx.icon("clock", class_name="h-3 w-3")),
            ("Quarantine", rx.icon("octagon-alert", class_name="h-3 w-3")),
            ("Out of Stock", rx.icon("circle-x", class_name="h-3 w-3")),
            rx.icon("circle", class_name="h-3 w-3"),
        ),
        rx.el.span(status, class_name="text-xs font-medium"),
        class_name=rx.match(
            status,
            (
                "Released",
                "inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-green-50 text-green-700 border border-green-200 w-fit",
            ),
            (
                "Pending Release",
                "inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
            ),
            (
                "Quarantine",
                "inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 w-fit",
            ),
            (
                "Out of Stock",
                "inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-gray-100 text-gray-600 border border-gray-200 w-fit",
            ),
            "inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-gray-100 text-gray-600 border border-gray-200 w-fit",
        ),
    )


def hazard_badge(
    is_hazard: rx.Var[bool], is_napza: rx.Var[bool]
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            is_napza,
            rx.el.span(
                rx.icon("shield-alert", class_name="h-3 w-3"),
                "NAPZA",
                class_name="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-purple-50 text-purple-700 border border-purple-200 w-fit",
            ),
            rx.fragment(),
        ),
        rx.cond(
            is_hazard,
            rx.el.span(
                rx.icon("triangle-alert", class_name="h-3 w-3"),
                "Hazard",
                class_name="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-orange-50 text-orange-700 border border-orange-200 w-fit",
            ),
            rx.fragment(),
        ),
        class_name="flex items-center gap-1",
    )


def stock_level_badge(
    on_hand: rx.Var[float], min_level: rx.Var[float]
) -> rx.Component:
    return rx.cond(
        on_hand <= 0,
        rx.el.span(
            "Critical",
            class_name="inline-flex px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 text-xs font-medium w-fit",
        ),
        rx.cond(
            on_hand < min_level,
            rx.el.span(
                "Low",
                class_name="inline-flex px-2 py-0.5 rounded-md bg-orange-50 text-orange-700 border border-orange-200 text-xs font-medium w-fit",
            ),
            rx.el.span(
                "OK",
                class_name="inline-flex px-2 py-0.5 rounded-md bg-green-50 text-green-700 border border-green-200 text-xs font-medium w-fit",
            ),
        ),
    )