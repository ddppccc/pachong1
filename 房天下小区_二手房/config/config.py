import math


# 百度坐标转高德
def baidu_chang_gaode(lat, lng):
    if not lat or not lng:
        return "", ""
    lng = float(lng)
    lat = float(lat)
    x_pi = 3.14159265358979324 * 3000.0 / 180.0

    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y,x) - 0.000003 * math.cos(x * x_pi)
    lng = z * math.cos(theta)
    lat = z * math.sin(theta)
    return lat, lng


if __name__ == '__main__':
    a = (1, 2, 3, [4, 5, 6, 7], 8)

    # a[2] = 2
    print(a[2])

