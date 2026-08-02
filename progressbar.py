import cv2

def draw_progress_bar(frame, x, y, width, height, percentage):

    # Background
    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (100, 100, 100),
        -1
    )

    # Filled Bar
    filled_width = int((percentage / 100) * width)

    cv2.rectangle(
        frame,
        (x, y),
        (x + filled_width, y + height),
        (0, 255, 0),
        -1
    )

    # Border
    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (255, 255, 255),
        2
    )

    # Percentage Text
    cv2.putText(
        frame,
        f"{percentage:.1f}%",
        (x + width + 10, y + height - 3),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )