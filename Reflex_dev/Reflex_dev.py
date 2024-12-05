"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from collections import Counter
from faker import Faker

# from rxconfig import config


class User(rx.Base):
    name: str
    email: str
    gender: str
    age: int


class Users(rx.State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_users()
        self.transform_users_for_display()

    users: list[User] = []
    users_for_display: list[dict] = []

    def generate_users(self):
        fake = Faker()
        self.users.clear()
        for i in range(10):
            self.users.append(
                User(
                    name=fake.name(),
                    email=fake.email(),
                    gender=fake.random_element(elements=("Male", "Female")),
                    age=fake.random_int(min=18, max=65),
                )
            )
        self.transform_users_for_display()

    def transform_users_for_display(self):
        gender_counter = Counter(user.gender for user in self.users)
        self.users_for_display = [{"name": gender, "count": count} for gender, count in gender_counter.items()]


def show_user(user: User):
    """Show a user in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        rx.table.cell(user.age),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def graph():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="count",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=Users.users_for_display,
        width="100%",
        height=250,
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.button("Generate Users", on_click=Users.generate_users, margin_bottom="1rem"),
            rx.text("Users by Gender"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Email"),
                        rx.table.column_header_cell("Gender"),
                        rx.table.column_header_cell("Age"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        Users.users,
                        show_user,
                    ),
                ),
                variant="surface",
            ),
            graph(),
        ),
    )


app = rx.App()
app.add_page(index)
