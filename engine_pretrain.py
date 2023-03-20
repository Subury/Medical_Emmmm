# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# --------------------------------------------------------
# References:
# DeiT: https://github.com/facebookresearch/deit
# BEiT: https://github.com/microsoft/unilm/tree/master/beit
# --------------------------------------------------------

from typing import Iterable

import torch

import util.misc as misc
import util.lr_sched as lr_sched


def train_one_epoch(model: torch.nn.Module,
                    data_loader: Iterable, optimizer: torch.optim.Optimizer,
                    device: torch.device, epoch: int, loss_scaler,
                    log_writer=None,
                    args=None):
    model.train(True)
    metric_logger = misc.MetricLogger(delimiter="  ")
    metric_logger.add_meter('lr', misc.SmoothedValue(window_size=1, fmt='{value:.6f}'))
    header = 'Epoch: [{}]'.format(epoch)
    print_freq = 20

    accum_iter = args.accum_iter

    optimizer.zero_grad()

    if log_writer is not None:
        print('log_dir: {}'.format(log_writer.log_dir))

    mask_ratio = args.mask_ratio
    for data_iter_step, batch in enumerate(metric_logger.log_every(data_loader, print_freq, header)):
        # we use a per iteration (instead of per epoch) lr scheduler
        if data_iter_step % accum_iter == 0:
            lr_sched.adjust_learning_rate(optimizer, data_iter_step / len(data_loader) + epoch, args)
        with torch.cuda.amp.autocast():
            loss, _, _ = model(batch, mask_ratio=mask_ratio)

            loss_value1 = loss[0].item()
            loss_value2 = loss[1].item()
            loss_value3 = loss[2].item()
            loss_value4 = loss[3].item()
            loss_value5 = loss[4].item()
            loss = loss[0] + loss[1] + loss[2] + loss[3] + loss[4]
            loss = loss / accum_iter
            loss_scaler(loss, optimizer, parameters=model.parameters(),
                        update_grad=(data_iter_step + 1) % accum_iter == 0)
            
            if (data_iter_step + 1) % accum_iter == 0:
                optimizer.zero_grad()

            torch.cuda.synchronize()

            metric_logger.update(loss1=loss_value1)
            metric_logger.update(loss2=loss_value2)
            metric_logger.update(loss3=loss_value3)
            metric_logger.update(loss4=loss_value4)
            metric_logger.update(loss5=loss_value5)

            lr = optimizer.param_groups[0]["lr"]
            metric_logger.update(lr=lr)

            loss_value_reduce1 = misc.all_reduce_mean(loss_value1)
            loss_value_reduce2 = misc.all_reduce_mean(loss_value2)
            loss_value_reduce3 = misc.all_reduce_mean(loss_value3)
            loss_value_reduce4 = misc.all_reduce_mean(loss_value4)
            loss_value_reduce5 = misc.all_reduce_mean(loss_value5)
            if log_writer is not None and (data_iter_step + 1) % accum_iter == 0:
                """ We use epoch_1000x as the x-axis in tensorboard.
                This calibrates different curves when batch size changes.
                """
                epoch_1000x = int((data_iter_step / len(data_loader) + epoch) * 1000)
                log_writer.add_scalar('train_loss1', loss_value_reduce1, epoch_1000x)
                log_writer.add_scalar('train_loss2', loss_value_reduce2, epoch_1000x)
                log_writer.add_scalar('train_loss3', loss_value_reduce3, epoch_1000x)
                log_writer.add_scalar('train_loss4', loss_value_reduce4, epoch_1000x)
                log_writer.add_scalar('train_loss5', loss_value_reduce5, epoch_1000x)
                log_writer.add_scalar('lr', lr, epoch_1000x)

    # gather the stats from all processes
    metric_logger.synchronize_between_processes()
    print("Averaged stats:", metric_logger)
    return {k: meter.global_avg for k, meter in metric_logger.meters.items()}