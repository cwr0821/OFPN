_base_ = [
    'rotated_faster_rcnn_r50_fpn_1x_dota_le90.py'
]

model = dict(
    backbone=dict(
        type='ResNeXt',
        depth=50,
        groups=32,
        base_width=4,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        style='pytorch',
        init_cfg=dict(
            type='Pretrained', checkpoint='open-mmlab://resnext50_32x4d')),
    neck=[
        dict(
            type='CA_PAFPN',
            in_channels=[256, 512, 1024, 2048],
            out_channels=256,
            num_outs=5
        ),
        dict(
            type='BFP',
            in_channels=256,
            num_levels=5,
            refine_level=2,
            refine_type='non_local')
    ],
    test_cfg=dict(
        rpn=dict(
            nms_across_levels=False,
            nms_pre=1000,
            nms_post=1000,
            max_num=1000,
            nms_thr=0.7,
            min_bbox_size=0),
        rcnn=dict(
            score_thr=0.05, nms=dict(type='soft_nms', iou_thr=0.5), max_per_img=120),
        keep_all_stages=False)
)