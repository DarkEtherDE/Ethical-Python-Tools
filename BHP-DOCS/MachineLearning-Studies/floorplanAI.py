import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_boxes(box_data):
    fig, ax = plt.subplots()

    for x, y, width, height in box_data:
        box = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='b', facecolor='r')  # Change facecolor to red
        ax.add_patch(box)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def main():
    box_data = []  # List to store box data

    while True:
        user_input = input("Enter box dimensions (x y width height) or 'finished' to exit: ")
        if user_input.lower() == 'finished':
            break

        try:
            x, y, width, height = map(float, user_input.split())
            box_data.append((x, y, width, height))  # Store box data
        except ValueError:
            print("Invalid input. Please provide four numeric values.")

    if box_data:
        generate_boxes(box_data)
        print("Stored box data:")
        for i, box in enumerate(box_data):
            print(f"Box {i+1}: x={box[0]}, y={box[1]}, width={box[2]}, height={box[3]}")
    else:
        print("No boxes to display.")

if __name__ == "__main__":
    main()
