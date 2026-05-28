def print_interactive_joints():
    selection = Gui.Selection.getSelection()
    if not selection:
        print("❌ Error: Please select an object in the tree first.")
        return

    target_part = selection[0]
    print(f"\n🔍 Searching for joints connected to: '{target_part.Label}'")
    print("=" * 60)

    # Global dictionary to store the found joints so you can reference them easily
    global found_joints
    found_joints = {}

    index = 1
    for obj in App.ActiveDocument.Objects:
        if hasattr(obj, "Reference1") and hasattr(obj, "Reference2"):
            part1 = obj.Reference1[0] if obj.Reference1 else None
            part2 = obj.Reference2[0] if obj.Reference2 else None

            if target_part in (part1, part2):
                other_part = part2 if target_part == part1 else part1
                other_label = other_part.Label if other_part else "None"

                # Save joint to our shortcut dictionary
                found_joints[index] = obj

                print(f"[{index}] 🔗 Joint: {obj.Label} (Connected to: '{other_label}')")
                index += 1

    if index == 1:
        print("ℹ️ No joints found connecting to this part.")
    else:
        print("=" * 60)
        print("👉 To JUMP to a joint in the tree, type: jump(1)")
        print("   (Replace '1' with the number of the joint you want to select)")

def jump(number):
    """Selects and focuses the chosen joint in the FreeCAD Tree View."""
    global found_joints
    if 'found_joints' not in globals() or not found_joints:
        print("❌ No joint list found. Please run print_interactive_joints() first.")
        return

    if number in found_joints:
        joint_obj = found_joints[number]

        # Clear current selection and select the target joint
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(joint_obj)

        print(f"✈️ Jumped to and highlighted '{joint_obj.Label}' in the Tree View!")
    else:
        print(f"❌ Invalid number. Choose a number between 1 and {len(found_joints)}")

# Run the finder immediately
print_interactive_joints()
