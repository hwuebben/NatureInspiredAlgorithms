import matplotlib.pyplot as plt
import numpy as np

def plot_evolution(results, nrBoxplots):
    plt.figure(figsize=(20,8))
    plt.title('Distribution of results for each generation')
    nrGenerations = results.shape[0]
    posBoxplots = np.arange(0, nrGenerations, int(nrGenerations/nrBoxplots))
    widthBoxplots = nrGenerations / (nrBoxplots * 2)
    plt.boxplot(np.rot90(results[posBoxplots,:]), widths=widthBoxplots, positions=posBoxplots)
    x = np.arange(results.shape[0]) + 1
    mean_scores = np.mean(results,axis=1)
    min_scores = np.min(results,axis=1)
    max_scores = np.max(results,axis=1)
    plt.fill_between(x, min_scores, max_scores, alpha=0.1, color='g', label='min/max')
    plt.plot(x, mean_scores, color='g', alpha=1, label='mean')
    plt.legend(loc=1)
    plt.show()

def plot3D_parameters(generations, gs):
    extract_genes = lambda gens, i, j: np.array([[ind.x[i:j] for ind in gen] for gen in gens])
    es = extract_genes(generations[gs], 0, 3)
    ss = extract_genes(generations[gs], 3, 6)
    ps = extract_genes(generations[gs], 6, 9)
    scores = np.array([[ind.targFuncVal for ind in gen] for gen in generations[gs]])

    for (g, e, s, p, score) in zip(gs, es, ss, ps, scores):
        fig = plt.figure(figsize=(16, 4))
        for i, (xs, x) in enumerate(((es, e), (ss, s), (ps, p))):
            ax = fig.add_subplot(131 + i, projection='3d')
            ax.scatter3D(x[:, 0], x[:, 1], x[:, 2], depthshade=False, c=score, cmap='Greens')
            ax.set_title(('e', 's', 'p')[i] + ' - generation: ' + str(g))
            ax.set_xlim(np.amin(xs[:, :, 0]), np.amax(xs[:, :, 0]))
            ax.set_ylim(np.amin(xs[:, :, 1]), np.amax(xs[:, :, 1]))
            ax.set_zlim(np.amin(xs[:, :, 2]), np.amax(xs[:, :, 2]))

        fig.tight_layout()
        plt.show()