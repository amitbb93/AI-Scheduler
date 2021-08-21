from . import algorithm

def adding_ids_to_array(final_shifts):
    final_shifts_ids = []
    c = 0
    for f in final_shifts:
        if f == 'admin':
            final_shifts_ids.append(["Empty", c])
        else:
            final_shifts_ids.append([f, c])
        c = c + 1
    return final_shifts_ids

def change_workers_shifts(request):
    updated_list = []
    for i in range(21):
        updated_list.append(request.POST[str(i)])
    algorithm.update_current_week(updated_list)
