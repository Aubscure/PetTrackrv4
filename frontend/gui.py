import customtkinter as ctk
from frontend.views.dashboard import create_dashboard
from frontend.views.add_pet_view import create_add_pet_view
from frontend.views.view_pets_tab import create_view_pets_tab
from frontend.views.pet_profile_tab import create_pet_profile_tab
from frontend.views.vaccination_visits_tab import VaccinationVisitsTab
from frontend.views.view_feeding_logs_tab import create_view_feeding_logs_tab
from frontend.views.grooming_logs_tab import create_grooming_logs_tab
from frontend.style.style import configure_table_style, apply_uniform_layout_style
from backend.controllers.grooming_controller import GroomingLogsController

def launch_gui():
    """Initializes the main application window and sets up dynamic view navigation."""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("PetTrackr")

    # Maximize the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Set a clean background color
    root.configure(fg_color="#F0F8FF")  # Light gray background

    navigation_stack = []

    def show_frame(name: str, from_back=False, **kwargs):
        """Show different frames based on the name."""
        if not from_back:
            navigation_stack.append((name, kwargs.copy()))

        # Clear the current frame
        for widget in root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        if name == "dashboard":
            create_dashboard(root, show_frame)
        elif name == "add_pet":
            create_add_pet_view(root, show_frame)
        elif name == "view_pets":
            create_view_pets_tab(root, show_frame)
        elif name == "pet_profile":
            pet = kwargs.get("pet")
            grooming_logs = GroomingLogsController().get_grooming_logs_for_pet(pet.id) if pet else []

            def go_back():
                if len(navigation_stack) > 1:
                    navigation_stack.pop()  # Remove current
                    prev_name, prev_kwargs = navigation_stack[-1]
                    show_frame(prev_name, from_back=True, **prev_kwargs)
                else:
                    show_frame("dashboard", from_back=True)

            create_pet_profile_tab(
                root,
                pet=pet,
                owner=kwargs.get("owner"),
                vet_visits=kwargs.get("vet_visits", []),
                vaccinations=kwargs.get("vaccinations", []),
                feeding_logs=kwargs.get("feeding_logs", []),
                grooming_logs=grooming_logs,
                show_frame=show_frame,
                go_back=go_back
            )
        elif name == "vaccination_visits":
            VaccinationVisitsTab.create(root, show_frame)
        elif name == "view_feeding_logs":
            create_view_feeding_logs_tab(root, show_frame)
        elif name == "grooming_logs":
            create_grooming_logs_tab(root, show_frame)

    configure_table_style()
    show_frame("dashboard")
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
