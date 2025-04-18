import flet as ft
import random
import asyncio

def main(page: ft.Page):
    # Define the Stack dimensions
    stack_width = 300  # Assumed width for the Stack
    stack_height = 250  # Height of the Stack
    container_size = 50  # Width and height of each container

    # Initial positions of the containers
    c1 = ft.Container(
        width=container_size,
        height=container_size,
        bgcolor="red",
        top=0,
        left=0,
        animate_position=1000  # Animation duration in milliseconds
    )

    c2 = ft.Container(
        width=container_size,
        height=container_size,
        bgcolor="green",
        top=60,
        left=0,
        animate_position=500
    )

    c3 = ft.Container(
        width=container_size,
        height=container_size,
        bgcolor="blue",
        top=120,
        left=0,
        animate_position=1000
    )

    # Add the containers to the page
    page.add(
        ft.Stack([c1, c2, c3], width=stack_width, height=stack_height)
    )

    # Function to move containers to random positions
    async def move_containers():
        max_top = stack_height - container_size  # 250 - 50 = 200
        max_left = stack_width - container_size  # 300 - 50 = 250

        while True:
            # Assign random positions to each container
            c1.top = random.randint(0, max_top)
            c1.left = random.randint(0, max_left)

            c2.top = random.randint(0, max_top)
            c2.left = random.randint(0, max_left)

            c3.top = random.randint(0, max_top)
            c3.left = random.randint(0, max_left)

            page.update()
            await asyncio.sleep(1)  # Wait 2 seconds before moving again

    # Start the automatic movement
    page.run_task(move_containers)

ft.app(main)