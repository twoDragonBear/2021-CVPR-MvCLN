import os
import imp
import random

import numpy as np
import torch
from loguru import logger
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

from alignment import euclidean_dist


def normalize(x):
    x = (x - np.tile(np.min(x, axis=0), (x.shape[0], 1))) / np.tile(
        (np.max(x, axis=0) - np.min(x, axis=0)), (x.shape[0], 1))
    return x


def random_index(n_all, n_train, seed):
    random.seed(seed)
    random_idx = random.sample(range(n_all), n_all)
    train_idx = random_idx[0:n_train]
    test_idx = random_idx[n_train:n_all]
    return train_idx, test_idx


def TT_split(n_all, test_prop, seed):
    '''
    split data into training, testing dataset
    '''
    random.seed(seed)
    random_idx = random.sample(range(n_all), n_all)
    train_num = np.ceil((1 - test_prop) * n_all).astype(np.int)
    train_idx = random_idx[0:train_num]
    test_num = np.floor(test_prop * n_all).astype(np.int)
    test_idx = random_idx[-test_num:]
    return train_idx, test_idx


def init_logger():
    log_dir = os.path.dirname(os.path.realpath(__file__))
    logger.info(log_dir)
    logger.add("%s/log/%s" % (log_dir, 'MvCLN.log'),
               rotation='16MB',
               encoding='utf-8',
               enqueue=True,
               retention='10 days')
    logger.info("Logging initialized.")


def svm_classify(data, label, test_prop, C):
    """
    trains a linear SVM on the data
    input C specifies the penalty factor of SVM
    """
    seed = random.randint(0, 1000)
    train_idx, test_idx = TT_split(data.shape[1], test_prop, seed)
    train_data = np.concatenate([data[0][train_idx], data[1][train_idx]],
                                axis=1)
    test_data = np.concatenate([data[0][test_idx], data[1][test_idx]], axis=1)
    test_label = label[test_idx]
    train_label = label[train_idx]

    clf = svm.LinearSVC(C=C, dual=False)
    clf.fit(train_data, train_label.ravel())

    p = clf.predict(test_data)
    test_acc = accuracy_score(test_label, p)
    return test_acc


def knn(data, label, test_prop, k):
    seed = random.randint(0, 1000)
    train_idx, test_idx = TT_split(data.shape[1], test_prop, seed)
    train_data = np.concatenate([data[0][train_idx], data[1][train_idx]],
                                axis=1)
    test_data = np.concatenate([data[0][test_idx], data[1][test_idx]], axis=1)
    test_label = label[test_idx]
    train_label = label[train_idx]

    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(train_data, train_label)
    p = clf.predict(test_data)
    test_acc = accuracy_score(test_label, p)
    return test_acc


def calculate_distance(model, train_pair_loader, args):
    model.eval()
    distance_0 = []
    distance_1 = []
    with torch.no_grad():
        for _, (x0, x1, labels) in enumerate(train_pair_loader):
            x0, x1, labels = x0.to(args.gpu), x1.to(args.gpu), labels.to(
                args.gpu)

            h0, h1 = model(x0.view(x0.size()[0], -1),
                           x1.view(x1.size()[0], -1))
            distance_0.append(h0)
            distance_1.append(h1)

    distance_0 = torch.cat(distance_0)
    distance_1 = torch.cat(distance_1)

    C = euclidean_dist(distance_0, distance_1)
    C = torch.softmax(C, 1)

    return C
