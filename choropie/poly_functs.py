def area_for_polygon(polygon):
    result = 0
    imax = len(polygon) - 1
    for i in range(0, imax):
        result += (polygon[i][1] * polygon[i + 1][0]) - (polygon[i + 1][1] * polygon[i][0])
    result += (polygon[imax][1] * polygon[0][0]) - (polygon[0][1] * polygon[imax][0])
    return result / 2.


def centroid_for_polygon(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) - 1

    result_x = 0
    result_y = 0
    for i in range(0, imax):
        result_x += (polygon[i][1] + polygon[i + 1][1]) * ((polygon[i][1] *
                                                            polygon[i + 1][0]) - (polygon[i + 1][1] * polygon[i][0]))
        result_y += (polygon[i][0] + polygon[i + 1][0]) * ((polygon[i][1] *
                                                            polygon[i + 1][0]) - (polygon[i + 1][1] * polygon[i][0]))
    result_x += (polygon[imax][1] + polygon[0][1]) * \
        ((polygon[imax][1] * polygon[0][0]) - (polygon[0][1] * polygon[imax][0]))
    result_y += (polygon[imax][0] + polygon[0][0]) * \
        ((polygon[imax][1] * polygon[0][0]) - (polygon[0][1] * polygon[imax][0]))
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)

    return result_y, result_x
