03/08/2023 16:11

数据准备:  
1. 预训练数据集 -- mimic_cxr
2. 预训练数据集划分 -- refers 工作中的数据划分
3. 分类数据集 -- NIH Chest X-Ray (14分类) [average acc]
4. 分割数据集 -- SIIM ACR Pneumothorax [dice socre]
5. 检测数据集 -- ⚠️ 目前没有找到比较通用的数据集和方法

图像预处理操作差异:
1. 标准化参数不同
2. MRM的图像预训练权重可能不是来自于imagenet，确实不是而是来自于MAE

正在进行中的实验:  
* ✅ 在V3版数据下，MRM的预训练  
* [] siim segmentation 任务的验证 (主要问题来自于原始数据集的丢失)
* [] convirt的代码复现  

03/20/2023 21:00

可能进行的改进:
* [] 对于医疗图像而言，**MAE**的重建目标什么是合适的 (Pixel or HOG or DINO) 
* [] **条件对比 NCE** 替换现有的对比学习损失, 同时 repair 两个分支

正在进行中的实验:
* [] **Deep-MRM**的验证实验，将**MAE**简单的替换为**Deep-MAE**，同时保留原有的Report分支

**喜马拉雅上的猴子🐒**: 
* 👌 Recent work shows that Validation loss in pretraining is a good indicator for how well a model will perform during fine-tuing on downstream tasks.[2]

**参考文献**:  
1. DeepMIM: Deep Supervision for Masked Image Modeling
2. On data scaling in masked image modeling

**实验记录**:
<table style="text-align: center">
    <tr></tr>
    <tr>
        <td >  </td>
        <td >  </td>
        <td >  </td>
        <td >  </td>
        <td >  </td>
        <td colspan='3'> 分类任务(NIH Chest X-Ray) </td>
        <td colspan='2'> 分割任务(SIIM ACR Pneumothorax) </td>
        <td> | </td>
        <td colspan='9'> 医疗报告补充实验 </td>
        <td> | </td>
        <td>  </td>
    </tr>
    <tr>
        <td> 序号 </td>
        <td> 方法 </td>
        <td> 描述 </td>
        <td> 预训练时间 </td>
        <td> 预训练日志</td>
        <td> 1%(LR) </td>
        <td> 10%(LR) </td>
        <td> 100%(LR) </td>
        <td> 10%(LR) </td>
        <td> 100%(LR) </td>
        <td> | </td>
        <td> BL-1 </td>
        <td> BL-2 </td>
        <td> BL-3 </td>
        <td> BL-4 </td>
        <td> MTR </td>
        <td> RG-L </td>
        <td> P </td>
        <td> R </td>
        <td> F1 </td>
        <td> | </td>
        <td> 实验状态 </td>
    </tr>
    <tr>
        <td> (1) </td>
        <td> convirt </td>
        <td>  </td>
        <td> xx(h)xx(m) </td>
        <td> /workspace/log/temp </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> 代码完成，思考训练 VIT or ResNet50 </td>
    </tr>
    <tr>
        <td> (2) </td>
        <td> refers </td>
        <td>  </td>
        <td> 30(h)30(m) </td>
        <td> /workspace/log/temp </td>
        <td> 73.4% (76.7%) </td>
        <td> 79.0% (80.9%) </td>
        <td> 82.3% (84.7%) </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> 预训练完成 分类完成</td>
    </tr>
    <tr>
        <td> (3) </td>
        <td> mrm </td>
        <td>  </td>
        <td> 61(h)50(m) </td>
        <td> /workspace/log/temp </td>
        <td> 79.2% (79.4%)</td>
        <td> 84.1% (84.0%)</td>
        <td> 86.0% (85.9%)</td>
        <td> 72.9% (73.2%)</td>
        <td>       (91.4%)</td>
        <td> | </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> 预训练完成 分类训练完成 分割100%数据未验证 </td>
    </tr>
    <tr>
        <td> (4) </td>
        <td> refers(mrm) </td>
        <td>  </td>
        <td> 3(h)55(m) </td>
        <td> /workspace/log/temp </td>
        <td> 76.6% (76.7%)</td>
        <td> 80.7% (80.9%)</td>
        <td> 83.8% (84.7%)</td>
        <td> 70.09 (72.1%)</td>
        <td>       (89.7%)</td>
        <td> | </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td> 预训练完成 分类训练完成 分割100%待验证 </td>
    </tr>
    <tr>
        <td> (5) </td>
        <td> deep mrm </td>
        <td>  </td>
        <td> xx(h)xx(m) </td>
        <td> /workspace/log/temp </td>
        <td> (79.4%)</td>
        <td> (84.0%)</td>
        <td> (85.9%)</td>
        <td> (73.2%)</td>
        <td> (91.4%)</td>
        <td> | </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> | </td>
        <td>   </td>
    </tr>
</table>