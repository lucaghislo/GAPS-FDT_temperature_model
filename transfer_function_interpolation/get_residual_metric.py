def residual_metric(resolution, residuals):
    diff = []

    for i in range(0, len(resolution)):
        delta = residuals[i] / resolution[i]
        diff.append(delta)
        # print(delta)

    return sum(diff), diff
