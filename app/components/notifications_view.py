import reflex as rx
from app.states.governance_state import GovernanceState


def severity_badge(sev: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        sev.upper(),
        class_name=rx.match(
            sev,
            (
                "high",
                "px-2 py-0.5 rounded-md text-[10px] font-bold bg-red-50 text-red-700 border border-red-200 w-fit",
            ),
            (
                "medium",
                "px-2 py-0.5 rounded-md text-[10px] font-bold bg-yellow-50 text-yellow-700 border border-yellow-200 w-fit",
            ),
            (
                "low",
                "px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200 w-fit",
            ),
            "px-2 py-0.5 rounded-md text-[10px] font-bold bg-gray-50 text-gray-700 border border-gray-200 w-fit",
        ),
    )


def filter_chip(label: str, value: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: GovernanceState.set_notification_filter(value),
        class_name=rx.cond(
            GovernanceState.notification_filter == value,
            "px-3 py-1.5 text-xs font-medium rounded-md bg-blue-600 text-white",
            "px-3 py-1.5 text-xs font-medium rounded-md bg-white text-gray-700 border border-gray-200 hover:bg-gray-50",
        ),
    )


def notifications_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bell", class_name="h-5 w-5 text-blue-600"),
                rx.el.div(
                    rx.el.div(
                        "Notifications",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        f"{GovernanceState.unread_notification_count} unread",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                filter_chip("All", "All"),
                filter_chip("Unread", "Unread"),
                filter_chip("High", "High"),
                filter_chip("Medium", "Medium"),
                filter_chip("Low", "Low"),
                rx.el.button(
                    rx.icon("check-check", class_name="h-3.5 w-3.5"),
                    "Mark all read",
                    on_click=GovernanceState.mark_all_read,
                    class_name="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-blue-700 hover:bg-blue-50 rounded-md ml-2",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex items-center justify-between p-4 border-b border-gray-200",
        ),
        rx.el.div(
            rx.cond(
                GovernanceState.filtered_notifications.length() > 0,
                rx.foreach(
                    GovernanceState.filtered_notifications,
                    lambda n: rx.el.div(
                        rx.el.div(
                            severity_badge(n["severity"]),
                            rx.cond(
                                ~n["read"],
                                rx.el.span(
                                    "•",
                                    class_name="text-blue-600 text-lg leading-none ml-1",
                                ),
                                rx.fragment(),
                            ),
                            rx.el.span(
                                n["timestamp"],
                                class_name="text-[10px] text-gray-500 ml-auto",
                            ),
                            class_name="flex items-center gap-1.5 mb-1",
                        ),
                        rx.el.div(
                            n["title"],
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.div(
                            n["message"],
                            class_name="text-xs text-gray-600 mt-0.5",
                        ),
                        rx.el.div(
                            rx.icon("user", class_name="h-3 w-3 text-gray-400"),
                            rx.el.span(
                                n["target_role"],
                                class_name="text-[10px] text-gray-500",
                            ),
                            rx.cond(
                                ~n["read"],
                                rx.el.button(
                                    "Mark as read",
                                    on_click=lambda: (
                                        GovernanceState.mark_notification_read(
                                            n["id"]
                                        )
                                    ),
                                    class_name="text-[10px] text-blue-600 hover:text-blue-700 ml-auto",
                                ),
                                rx.fragment(),
                            ),
                            class_name="flex items-center gap-1 mt-2",
                        ),
                        class_name=rx.cond(
                            n["read"],
                            "px-4 py-3 border-b border-gray-100 last:border-b-0",
                            "px-4 py-3 border-b border-gray-100 last:border-b-0 bg-blue-50/40",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.icon(
                        "bell-off", class_name="h-10 w-10 text-gray-300 mx-auto"
                    ),
                    rx.el.div(
                        "No notifications match this filter.",
                        class_name="text-sm text-gray-500 mt-2 text-center",
                    ),
                    class_name="px-4 py-12 text-center",
                ),
            ),
            class_name="max-h-[600px] overflow-y-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-lg overflow-hidden",
    )