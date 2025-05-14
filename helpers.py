from models import OrderStatus


def get_next_status(current):
    flow = [
        OrderStatus.AWAITING.value,
        OrderStatus.CONFIRMED.value,
        OrderStatus.PREPARING.value,
        OrderStatus.READY.value,
        OrderStatus.COMPLETED.value,
    ]
    try:
        index = flow.index(current)
        return flow[index + 1] if index + 1 < len(flow) else current
    except ValueError:
        return current  # fallback if unknown status
