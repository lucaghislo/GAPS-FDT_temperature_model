def residual_metric(resolution, residuals, x):
    diff = []

    for i in range(0, len(resolution)):
        delta = residuals[i] - resolution[i]
        diff.append(delta)
        # if delta > 0:
        #     diff.append(delta * (1 / (x[i])))
        # else:
        #     diff.append(0)

    return sum(diff)
