from datetime import datetime
def new_batch_number(previous_batch_id):
    # prev 031020261150-001
    today = datetime.now().strftime("%d-%m-%Y-%H-%M")
    day, month, year, hour, minute = today.split("-")

    increase_by_one = 1
    if previous_batch_id:
        previous_count = previous_batch_id.split("-")[1]
        increase_by_one = int(previous_count) + 1

    reformat = f"{day}{month}{year}{hour}{minute}-" + str(increase_by_one).zfill(3)

    return reformat

