from ..constants import *
import random


def get_deps(weights, expand=0.0):
    deps = []
    for dep_mat, dep in (
            (weights.dep_fixing, DEP_FIXING),
            (weights.dep_reinforcing, DEP_REINFORCING)):
        for i in range(weights.n):
            for j in range(weights.n):
                if dep_mat[i, j] != 0 or (random.random() < expand and i != j):
                    deps.append((i, j, dep))

    return deps


def get_all_deps(n, dep_similar=False, dep_exclusive=False):
    """
    Convenience method for getting a list of all dependencies to consider learning for a given number of labeling
    functions.

    No self dependencies are included, i.e., (i, i, _). In cases of symmetric dependencies, e.g., DEP_SIMILAR, only the
    first case, (i, j, _) where i < j, is included.

    :param n: number of labeling functions
    :param dep_similar: whether to include DEP_SIMILAR dependencies. Default is False.
    :param dep_exclusive: whether to include DEP_DEP_EXCLUSIVE dependencies. Default is False.
    """
    deps = []

    # Symmetric dependencies
    if dep_similar and dep_exclusive:
        sym_deps = (DEP_SIMILAR, DEP_EXCLUSIVE)
    elif dep_similar:
        sym_deps = (DEP_SIMILAR,)
    elif dep_exclusive:
        sym_deps = (DEP_EXCLUSIVE,)
    else:
        sym_deps = ()

    for dep in sym_deps:
        for i in range(n):
            for j in range(i + 1, n):
                deps.append((i, j, dep))

    # Asymmetric dependencies
    for dep in (DEP_FIXING, DEP_REINFORCING):
        for i in range(n):
            for j in range(n):
                if i != j:
                    deps.append((i, j, dep))

    return deps
