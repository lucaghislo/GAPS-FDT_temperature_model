def compute_weigths(initial_weights, residuals, resolution, x):

    res_res_difference = []

    for i in range(0, len(residuals)):
        difference = (residuals[i] - resolution[i]) / resolution[i]
        res_res_difference.append(difference)

    weights = []

    for i in range(0, len(initial_weights)):
        if res_res_difference[i] > 0:
            weights.append(
                initial_weights[i]
                + (res_res_difference[i] / (x[i])) * initial_weights[i]
            )
        else:
            # weights.append(
            #     initial_weights[i] - res_res_difference[i] * initial_weights[i]
            # )
            weights.append(initial_weights[i])

    return weights
