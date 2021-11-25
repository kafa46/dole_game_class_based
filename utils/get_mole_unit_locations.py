def get_mole_locations(frame, divide_unit):
    
    # pos_x, pos_y = loc[0], loc[1]
    frame_height, frame_width, _ = frame.shape
    
    # Calculate unit-distance 
    unit_dist_x = frame_width / divide_unit
    unit_dist_y = frame_height / divide_unit
    
    unit_dist_x_list = [unit_dist_x] * divide_unit
    unit_dist_y_list = [unit_dist_y] * divide_unit
    
    # Get mole grid ID
    x_list = []
    for x, unit_x in enumerate(unit_dist_x_list):
        x_start = x * unit_x
        x_end = x_start + unit_x 
        x_list.append((x_start, x_end))
        
    y_list = []
    for y, unit_y in enumerate(unit_dist_y_list):
            y_start = y * unit_y
            y_end = y * unit_y + unit_y 
            y_list.append((y_start, y_end))
    
    unit_map = []
    for y_range in y_list:
        for x_range in x_list:
            unit_map.append((x_range, y_range))
    
    
    return unit_map