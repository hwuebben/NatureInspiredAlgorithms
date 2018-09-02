import matplotlib.pyplot as plt
import numpy as np

def plot_evolution(results, nrBoxplots):
    plt.figure(figsize=(20,8))
    plt.title('Distribution of results for each generation')
    nrGenerations = results.shape[0]
    posBoxplots = np.arange(0, nrGenerations, int(nrGenerations/nrBoxplots))
    widthBoxplots = nrGenerations / (nrBoxplots * 2)
    plt.boxplot(np.rot90(results[posBoxplots,:]), widths=widthBoxplots, positions=posBoxplots)
    x = np.arange(results.shape[0])
    mean_scores = np.mean(results,axis=1)
    min_scores = np.min(results,axis=1)
    max_scores = np.max(results,axis=1)
    plt.fill_between(x, min_scores, max_scores, alpha=0.1, color='g', label='min/max')
    plt.plot(x, mean_scores, color='g', alpha=1, label='mean')
    plt.legend(loc=1)
    plt.show()