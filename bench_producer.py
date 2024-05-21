import glob
import os
import re
import shutil
import subprocess

# orig_bench = 'lol/circuit-synthesis/iwls2023/submissions/google/aig_bench_1/ex62.bench'
# new_bench = 'ex55_from_ex62.bench'
# substitution = {0: (5, 0), 1: (0, 1), 2: (3, 1), 3: (1, 0), 4: (2, 1), 5: (7, 0), 6: (4, 1), 7: (14, 1), 8: (15, 1), 9: (9, 1), 10: (8, 1), 11: (10, 0), 12: (11, 1), 13: (13, 1), 14: (6, 0), 15: (12, 1)}
# outs = [('out', 0, 0)]


info = [
    ('ex00', 'ex93', '[1=!12, 2=!4, 3=15, 4=!3, 5=!2, 6=7, 7=!14, 8=!8, 9=!10, 10=!0, 11=!9, 12=!5, 13=!11, 14=1, 15=!13] [2, 8, !0, 0, 0, !11, 5, 9, x0, 7, !x1, 3, 11, 12]'),
    ('ex01', 'ex42', '[0=13, 1=!12, 2=!15, 5=11, 7=5, 8=!10, 9=1, 10=7, 11=!4, 12=!6, 13=14, 14=!9] [!x8, x3, !x6, !4, 6, 3, !x4]'),
    ('ex02', 'ex10', '[0=0, 1=3, 2=2, 3=4, 4=6, 5=7, 7=8, 8=!9] [5, 8, 8, 8, 3, !2, !4, !0, !x9, x6, !9, 6, 8]'),
    ('ex03', 'ex17', '[0=1, 1=!7, 3=!2, 4=5, 5=!4, 6=0, 7=3] [!0, !x2, 1]'),
    ('ex04', 'ex92', '[0=9, 1=1, 2=!6, 5=!8, 7=4, 8=7, 9=!12, 10=11, 11=!0, 12=13, 13=5, 14=!3] [!x8, x3, !x6, 1, !4, 2, !x4]'),
    ('ex05', 'ex47', '[0=8, 1=2, 2=3, 5=5, 6=!6, 7=0, 8=!4, 9=1] [!x0, x3, !8, 9, !x3, 7, !1, 3, 4, !x4, !0]'),
    ('ex06', 'ex22', '[0=!3, 1=!7, 2=!4, 3=!6, 4=!8, 5=1, 7=!9, 8=!5] [!8, !0, !0, !0, 2, !4, 10, !5, !x9, x6, 6, 7, !0]'),
    ('ex07', 'ex36', '[0=0, 1=4, 2=2, 3=3, 4=1, 5=6, 6=10, 7=7, 8=13, 10=5, 12=14, 13=!9, 14=11, 15=15] [0, 15, x3, x8, x3, 14, !5, x11, 1, 8, 7, !10, !x15, 19, !9, 6, !x9, 3, 2, !2, !9, 5, 18]'),
    ('ex08', 'ex45', '[0=0, 1=2, 2=4, 3=1, 4=5, 5=6, 6=7, 8=10, 10=!9, 11=!8, 12=!12] [5, !12, !x3, !11, x9, !0, x8, x7, !2, !0, !7, 4, 1, 14, !6, !1, 3]'),
    ('ex09', 'ex58', '[0=8, 1=!6, 2=!1, 5=!3, 7=!2, 8=!5, 9=12, 10=15, 11=13, 12=!10, 13=9, 14=14] [!x8, x3, !x6, !3, !1, !0, !x4]'),
    ('ex10', 'ex57', '[0=3, 1=1, 3=2, 4=0, 5=5, 7=6, 8=8, 9=10, 10=9] [x6, 0, x2]'),
    ('ex11', 'ex38', '[0=4, 1=8, 2=9, 3=0, 4=5, 5=11, 6=7, 9=1, 10=12, 12=!10, 13=6, 14=3] [!0, !x11, !11, !17, 3, x6, !1, !7, !8, !14, 4, !12, !7, 11, x7, 5, 6, !3, !x8]'),
    ('ex12', 'ex74', '[0=12, 1=6, 2=!4, 5=!3, 7=10, 8=!5, 9=0, 10=7, 11=14, 12=!13, 13=15, 14=!1] [!x8, x3, !x6, !1, 2, !6, !x4]'),
    ('ex13', 'ex52', '[1=1, 2=5, 3=!0, 4=!4, 5=!7, 6=!2, 7=!3] [!3, x0, !4, !10, 3, x5, 1, !2, !11, 12, 8, 12, !8, !x6, 5, !12]'),
    ('ex14', 'ex35', '[0=2, 1=0, 2=6, 4=!3, 6=!5, 7=!1, 8=4, 9=!8] [!0, !x3, x5]'),
    ('ex15', 'ex73', '[0=!8, 1=!5, 2=7, 5=!11, 7=14, 8=0, 9=4, 10=!3, 11=9, 12=1, 13=!6, 14=10] [!x8, x3, !x6, 4, 1, !5, !x4]'),
    ('ex16', 'ex07', '[0=1, 2=2, 3=0, 4=!4, 5=!5] [0, x1, !2, !1]'),
    ('ex17', 'ex67', '[0=!12, 1=!1, 2=13, 5=6, 7=!10, 8=!2, 9=!0, 10=!14, 11=7, 12=8, 13=!5, 14=!15] [!x8, x3, !x6, 0, 7, !1, !x4]'),
    ('ex18', 'ex40', '[0=4, 1=!2, 2=!12, 4=7, 5=10, 6=!9, 7=!11, 8=8, 9=1, 10=!6, 11=!3] [3, 3, x3, !0, !x12, 1]'),
    ('ex19', 'ex12', '[0=4, 1=1, 2=2, 3=5, 4=3] [!0, x5]'),
    ('ex20', 'ex29', '[0=5, 1=11, 2=!7, 5=4, 7=8, 8=10, 9=12, 10=14, 11=0, 12=!13, 13=!6, 14=!2] [!x8, x3, !x6, 2, 5, 1, !x4]'),
    ('ex21', 'ex51', '[0=4, 1=!2, 2=!11, 3=0, 4=!3, 5=6, 6=13, 7=14, 8=!10, 9=1, 10=!8, 11=9, 12=!5, 13=!7, 14=12, 15=15] [0, 4, !2, !1, x15, !x5]'),
    ('ex22', 'ex94', '[0=!7, 1=14, 2=6, 3=2, 4=8, 5=!4, 6=11, 7=1, 8=5, 9=!12, 10=3, 11=!13, 12=0, 13=!10, 14=15, 15=!9] [40, !48, 9, 10, !2, x6, 11, !46, x14, !56, 38, !59, !13, !44, 0, !37, !33, 49, 50, !8, 13, !42, !34, 36, !21, !3, 54, 23, 36, !9, !13, x10, 58, !x12, x13, 29, x7, 39, 16, !37, !x9, 6, !1, 12, !x13, 45, x14, 55, 9, !18, !54, 35, x6, 15, 30, !0, !5, !60, !47, !27, !24, !24, 32, 14, 47, !50, !24, 13, !7]'),
    ('ex23', 'ex04', '[0=8, 1=5, 2=!1, 5=!9, 6=!7, 7=!3, 8=4, 9=!0] [!x0, x3, !1, !4, !x3, 5, !0, 8, 3, !x4, 7]'),
    ('ex24', 'ex37', '[0=5, 1=4, 2=!1, 5=7, 7=3, 8=!10, 9=!0, 10=6, 11=!8, 12=2, 13=!11, 14=!14] [!x8, x3, !x6, !6, !4, !5, !x4]'),
    ('ex25', 'ex15', '[0=!7, 1=!4, 2=!11, 4=!6, 5=!5, 6=!9, 8=!0, 9=!10, 10=!1, 11=!8] [!4, !16, !14, 5, 9, 12, !14, !5, !7, 0, !16, !2, x3, 14, x10, x7, 10]'),
    ('ex26', 'ex81', '[0=14, 1=3, 2=5, 5=!12, 7=!2, 8=9, 9=6, 10=8, 11=!13, 12=11, 13=7, 14=!15] [!x8, x3, !x6, !5, 3, 2, !x4]'),
    ('ex27', 'ex01', '[0=12, 1=!13, 2=9, 5=6, 7=1, 8=7, 9=11, 10=8, 11=5, 12=!4, 13=!0, 14=2] [!x8, x3, !x6, !3, 2, 1, !x4]'),
    ('ex28', 'ex33', '[0=1, 1=!7, 2=!5, 5=!4, 7=14, 8=12, 9=0, 10=!9, 11=11, 12=!3, 13=2, 14=10] [!x8, x3, !x6, 3, 2, 1, !x4]'),
    ('ex29', 'ex44', '[0=!3, 2=!5, 3=7, 4=0, 5=!6, 7=!8, 8=!1, 9=2] [!x6, !0, !x1, 0, 1]'),
    ('ex30', 'ex05', '[0=3, 1=9, 2=11, 5=8, 7=!4, 8=!13, 9=0, 10=7, 11=2, 12=12, 13=5, 14=!1] [!x8, x3, !x6, !0, !3, !5, !x4]'),
    ('ex31', 'ex09', '[0=5, 1=4, 2=!10, 3=3, 4=!1, 5=!0, 6=!2, 7=8, 8=!6, 10=7, 12=9, 13=11, 14=13, 15=12] [!5, !18, x3, x8, x3, !4, 8, x11, 15, !0, 6, !7, !x15, 13, !14, !11, !x9, 17, 1, !1, !14, !8, 9]'),
    ('ex32', 'ex06', '[0=4, 1=!8, 2=0, 5=11, 7=!1, 8=5, 9=2, 10=!6, 11=!10, 12=3, 13=9, 14=!7] [!x8, x3, !x6, !3, 4, !1, !x4]'),
    ('ex33', 'ex66', '[0=5, 1=!7, 2=14, 3=13, 4=11, 5=1, 6=9, 7=!0, 8=!15, 9=!4, 10=!8, 11=2, 12=!12, 13=6, 14=!10, 15=3] [3, 2, 0, 1, x15, !x5]'),
    ('ex34', 'ex91', '[0=2, 1=1, 2=!7, 5=8, 7=!6, 8=5, 9=!14, 10=9, 11=3, 12=!4, 13=!12, 14=!13] [!x8, x3, !x6, !3, 4, 5, !x4]'),
    ('ex35', 'ex79', '[0=0, 1=3, 2=1, 3=5, 4=4, 5=!6] [1, !3, !5, !2, !0, 5, 2, x6, !9, !5]'),
    ('ex36', 'ex98', '[0=2, 1=0, 2=6, 3=10, 4=12, 5=3, 6=15, 7=8, 8=!9, 9=!4, 11=11, 12=5, 13=!13, 14=!14, 15=!7] [0, !x10]'),
    ('ex37', 'ex69', '[0=0, 1=1, 2=3, 3=2, 4=6, 5=9, 6=11, 7=8, 9=14, 10=4, 11=15, 13=!5, 14=12] [14, !3, 9, !2, !x8, 5, x15, !11, !8, !x12, 8, !1, !8, !4, !6, !x3, x3, 10, !12, 2, !15]'),
    ('ex38', 'ex86', '[0=!9, 1=1, 2=!12, 3=0, 5=!2, 6=10, 7=!4, 8=!5, 9=6, 10=!3] [!x4, x11, 2]'),
    ('ex39', 'ex56', '[0=0, 1=3, 2=2, 3=5, 4=8, 5=9, 6=6, 7=7, 8=11, 9=1, 10=12, 11=13, 12=14, 14=4, 15=15] [!x10, !8, 19, !14, !0, 6, !20, !19, !1, !10, !11, !x10, !x13, !15, !16, !2, !20, x0, 13, !19, !7, 4, !x12]'),
    ('ex40', 'ex48', '[0=2, 2=1, 3=!9, 4=7, 6=!0, 7=3, 8=10, 9=!8, 10=5] [2, !7, !x5, !9, 10, 6, !16, 8, !13, 15, 11, !x4, !15, !9, !5, 18, !x8, 4, 16, !8, 3, 20, 12, x10, 21, !11, !1, !x1, x6]'),
    ('ex41', 'ex25', '[0=12, 1=!14, 3=9, 4=1, 5=!11, 6=4, 7=!0, 8=10, 9=!13, 10=5, 12=!8, 14=3] [x13, x11, !2, !x2]'),
    ('ex42', 'ex49', '[0=0, 1=4, 2=5, 3=6, 4=8, 5=1, 6=9, 7=2, 9=10, 10=11, 11=!13] [1, x8, !x12]'),
    ('ex43', 'ex26', '[0=!14, 1=12, 2=!2, 3=13, 4=0, 5=!3, 6=11, 7=6, 8=!15, 10=!9, 12=8, 13=4, 14=5, 15=!1] [!6, !12, x3, x8, x3, 13, 14, x11, !4, !10, 18, 11, !x15, 2, 5, !16, !x9, 17, !0, 0, 5, !14, !9]'),
    ('ex44', 'ex75', '[0=7, 1=13, 2=6, 5=!5, 7=1, 8=!15, 9=!2, 10=!10, 11=0, 12=9, 13=!3, 14=8] [!x8, x3, !x6, 0, 3, 1, !x4]'),
    ('ex45', 'ex46', '[0=4, 1=!8, 2=9, 4=!7, 5=10, 6=!6, 7=!11, 8=!12, 9=2, 10=!0, 11=5] [!5, !5, x3, 0, !x12, x0]'),
    ('ex46', 'ex03', '[0=0, 1=1, 2=3, 3=6, 5=11, 6=8, 7=9, 9=10, 10=5, 12=14, 13=15, 14=12, 15=13] [x11, 3, !x8, x4]'),
    ('ex47', 'ex84', '[0=6, 1=2, 2=0, 3=13, 4=4, 5=11, 6=10, 7=9, 8=!7, 9=15, 10=!3, 11=8, 12=1, 13=!12, 14=14, 15=5] [4, !0, 1, 3, x15, !x5]'),
    ('ex48', 'ex78', '[0=!0, 1=6, 2=!7, 3=!5, 4=!1, 5=8, 7=!2, 8=!3] [!6, 8, 8, 8, 4, !10, !7, !9, !x9, x6, 0, !5, 8]'),
    ('ex49', 'ex30', '[0=!3, 1=!9, 2=4, 3=5, 7=0, 8=6, 9=!8] [x6, !0, 0, !2, x5, !x4]'),
    ('ex50', 'ex61', '[0=!12, 1=!0, 2=!1, 5=2, 7=!7, 8=!6, 9=!4, 10=11, 11=!8, 12=13, 13=10, 14=3] [!x8, x3, !x6, 1, !2, 4, !x4]'),
    ('ex51', 'ex28', '[0=5, 1=11, 2=6, 5=!12, 7=13, 8=!10, 9=!4, 10=!9, 11=!2, 12=14, 13=0, 14=!1] [!x8, x3, !x6, !0, !2, 3, !x4]'),
    ('ex52', 'ex82', '[0=!14, 1=!2, 2=!5, 3=!0, 4=4, 5=!15, 6=9, 7=!11, 8=12, 9=7, 11=3, 12=1, 14=6, 15=!8] [11, !11, 0, !x13, 9, 1, 11, x4, !x10, 6, !3, !11, !8, 4]'),
    ('ex53', 'ex68', '[0=!7, 1=5, 2=!8, 3=!2, 6=!10, 7=!11, 8=0, 9=6, 10=!9, 11=4] [2, !4, 6, !x10, 1, !x5, !x4, !x11]'),
    ('ex54', 'ex60', '[0=6, 1=0, 2=!12, 5=!14, 7=5, 8=!3, 9=!8, 10=!4, 11=7, 12=!13, 13=2, 14=!9] [!x8, x3, !x6, !1, !3, !5, !x4]'),
    ('ex55', 'ex62', '[0=5, 1=!0, 2=!3, 3=1, 4=!2, 5=7, 6=!4, 7=!14, 8=!15, 9=!9, 10=!8, 11=10, 12=!11, 13=!13, 14=6, 15=!12] [0]'),
    ('ex56', 'ex87', '[0=!1, 1=!6, 2=!3, 5=12, 7=9, 8=13, 9=!4, 10=!2, 11=!0, 12=!11, 13=8, 14=!7] [!x8, x3, !x6, !4, !0, 3, !x4]'),
    ('ex57', 'ex70', '[0=!4, 1=!6, 2=!13, 5=3, 7=11, 8=!10, 9=!5, 10=!8, 11=12, 12=1, 13=!9, 14=7] [!x8, x3, !x6, !0, 3, !2, !x4]'),
    ('ex58', 'ex77', '[0=!10, 1=6, 2=!11, 5=!7, 7=3, 8=!2, 9=9, 10=!12, 11=!14, 12=8, 13=13, 14=!5] [!x8, x3, !x6, !3, 5, !0, !x4]'),
    ('ex59', 'ex99', '[0=4, 1=6, 2=!1, 3=!5, 4=!2, 5=3] [!x6, !1]'),
    ('ex60', 'ex32', '[0=4, 1=2, 2=!1, 3=0, 4=!5, 5=6] [!x6, 1]'),
    ('ex61', 'ex97', '[0=6, 1=9, 2=8, 3=2, 4=!4, 6=!7, 7=0, 8=!5, 10=1] [!x3, 1, !x5, !5, !4, 6, x9, !0, x8]'),
    ('ex62', 'ex76', '[0=13, 1=!6, 2=12, 5=10, 7=!9, 8=!0, 9=!7, 10=14, 11=4, 12=!8, 13=!3, 14=!11] [!x8, x3, !x6, !2, 4, 0, !x4]'),
    ('ex63', 'ex90', '[0=3, 2=!6, 3=2, 4=9, 5=5, 7=!1, 8=!7, 9=!8] [!x6, !1, !x1, 1, 3]'),
    ('ex64', 'ex19', '[0=7, 1=8, 2=!0, 4=!6, 6=!3, 7=!1, 8=!4, 9=2] [!1, !x3, x5]'),
    ('ex65', 'ex50', '[0=13, 1=8, 2=9, 3=!5, 4=15, 6=!2, 8=!7, 9=1, 10=0, 11=11, 12=10, 13=!14, 14=4, 15=12] [!1, !x9, 2, x5, !4, x7, 6]'),
    ('ex66', 'ex96', '[0=0, 2=!4, 3=8, 4=5, 5=9, 7=6, 8=7, 9=!3] [!x6, 0, !x1, !0, 1]'),
    ('ex67', 'ex95', '[0=0, 1=1, 2=2, 3=!3, 4=!4, 5=!6, 6=7] [6, !1, 7, x6, !x6, 8, x0, 4, !0, !x7, !2]'),
    ('ex68', 'ex11', '[0=!13, 1=!2, 2=6, 5=!5, 7=1, 8=!7, 9=!11, 10=9, 11=10, 12=!0, 13=!3, 14=8] [!x8, x3, !x6, !4, 6, !2, !x4]'),
    ('ex69', 'ex24', '[0=!3, 1=6, 2=0, 3=!5, 4=4, 7=7, 8=2, 9=!1] [54, 38, !69, 76, !x3, !x7, 51, !63, 18, !68, !8, !x8, !57, 78, !65, !31, !71, !50, !67, !32, 36, x3, 10, !56, 48, 4, 50, 31, x2, 3, !76, !25, 59, 66, !5, !64, 33, !73, x4, !66, 71, !41, 10, !x9, !0, !x0, x4, !56, !x1, 2, 75, !9, 44, !13, !x2, 47, 17, !21, !34, !46, !55, 15, 1, x4, 53, 11, !24, !6, 48, 4, !19, !38, !x5, !16, 29, !46, 20, 15, 26, !72, 45, !7, !x2, !14, 64, !24, !57, !77, !30, !43, 43, 22, !x6, !x7, !28]'),
    ('ex70', 'ex39', '[0=1, 1=2, 4=0, 5=8, 6=!4, 7=5, 8=!6, 9=!3] [x3, 2, !x2, 3, !1, 4, x5]'),
    ('ex71', 'ex65', '[0=4, 1=0, 2=5, 3=!2, 4=3] [27, 20, !5, !6, 22, !13, 30, 10, !26, !x0, 36, !18, !5, !5, !2, !4, x5, 33, !32, 26, 35, x1, !x3, !34, 14, !x0, x1, 12, !27, !34, 39, 25, !33, 11, 37, 28, !10, 38, 17, !7, !15, !15]'),
    ('ex72', 'ex41', '[0=!2, 1=3, 2=!1, 4=!4, 5=!0] [!0, !x2, !2, x3, !4, !3, x5, !5]'),
    ('ex73', 'ex16', '[0=!3, 1=!10, 2=!13, 5=12, 7=6, 8=7, 9=8, 10=!1, 11=!4, 12=5, 13=11, 14=9] [!x8, x3, !x6, 2, !3, 4, !x4]'),
    ('ex74', 'ex43', '[0=!5, 1=!14, 2=11, 5=!4, 7=!2, 8=!9, 9=!6, 10=!3, 11=!1, 12=!0, 13=!7, 14=!8] [!x8, x3, !x6, 5, 0, !2, !x4]'),
    ('ex75', 'ex23', '[1=1, 2=4, 3=3, 4=2, 5=!6, 6=7, 7=!8] [1, x0]'),
    ('ex76', 'ex83', '[0=0, 1=3, 4=7, 5=5, 6=!6, 7=!2, 8=9, 9=!10, 10=11] [!7, 13, !9, 6, !5, 2, 10, 0, x3, x2, !x7, !5, 7, !5, 4]'),
    ('ex77', 'ex54', '[0=!1, 1=!2, 2=12, 5=!4, 7=5, 8=8, 9=!11, 10=6, 11=13, 12=14, 13=!0, 14=3] [!x8, x3, !x6, 4, 1, 5, !x4]'),
    ('ex78', 'ex85', '[0=!1, 1=!4, 2=!13, 5=!3, 7=!14, 9=9, 10=6, 11=!2, 12=5, 13=15, 14=11] [!x8, x3, !x6, 1, !2, 3, !x4]'),
    ('ex79', 'ex18', '[1=6, 2=9, 3=0, 4=3, 5=!5, 7=2, 8=8, 9=!4, 10=!11, 11=!7] [x2, 5, 100, !43, 84, !81, 67, !29, 28, !23, !76, !69, x6, !52, !74, !52, !30, !33, !8, 94, !88, x1, !80, 11, x1, 22, !49, 72, !37, 45, 16, 93, !99, 45, 54, 66, !63, 38, 53, 17, !x1, !53, 28, !4, !82, 102, 59, 95, 30, !10, x6, !70, 86, 53, 37, !9, 24, 71, !55, !81, 50, !68, !x4, !66, 38, 21, 100, x1, 100, x1, 22, 98, !60, 65, !19, !41, !x0, 66, x2, !12, !64, 25, 89, 2, !47, !44, x2, !33, x8, x6, !97, !40, !36, 7, !96, 61, 7, !48, !42, !57, !x7, 72, !x7, !91, !92, 14, x8, !62, 80, 5, !21, !87, 53, 15, !89]'),
    ('ex80', 'ex89', '[0=!1, 1=5, 4=3, 5=6, 6=!7, 7=8] [!x2, !x8, 2, !1, !1, !x3, !x9]'),
    ('ex81', 'ex27', '[0=!6, 1=!3, 2=!4, 5=7, 7=!2, 8=0, 9=!12, 10=!8, 11=5, 12=9, 13=13, 14=!1] [!x8, x3, !x6, !0, 4, 1, !x4]'),
    ('ex82', 'ex55', '[0=!5, 1=!10, 2=6, 3=!2, 5=4, 6=!8, 7=11, 8=0, 9=1, 10=!9] [!x4, x11, 0]'),
    ('ex83', 'ex53', '[0=0, 1=1, 3=2, 4=3, 5=4, 7=6, 8=5, 9=7, 10=!8] [x6, !0, x2]'),
    ('ex84', 'ex20', '[0=12, 1=!1, 2=0, 5=11, 7=!15, 8=10, 9=7, 10=!3, 11=8, 12=6, 13=!5, 14=9] [!x8, x3, !x6, 1, 4, 5, !x4]'),
    ('ex85', 'ex80', '[0=!1, 1=13, 2=12, 5=!6, 7=!2, 8=!14, 9=!15, 10=7, 11=10, 12=!0, 13=8, 14=11] [!x8, x3, !x6, !3, !5, !0, !x4]'),
    ('ex86', 'ex21', '[0=10, 1=!2, 2=11, 3=8, 4=!4, 5=9, 6=3, 7=!0, 10=!5, 11=!6] [!4, x9, 0, 3, !0, !x8]'),
    ('ex87', 'ex59', '[0=0, 1=1, 2=2, 3=3, 4=4, 5=6, 6=5, 7=7, 8=11, 9=12, 10=10, 11=13, 12=9, 13=15, 14=!14, 15=!8] [!9, 9, !6, !18, !2, 15, !15, !3, !2, !5, !13, 9, !0, !12, !8, 11, 23, !3, 21, x11, !1, x0, !10, !10]'),
    ('ex88', 'ex02', '[0=!2, 1=6, 2=7, 3=!11, 4=!4, 5=9, 6=3, 7=1, 8=13, 9=!10, 10=5, 11=!0, 13=!14, 14=!12, 15=15] [0, !x9, 1, x5, !3, !x12, 2]'),
    ('ex89', 'ex00', '[2=!6, 4=9, 5=!0, 8=1, 9=!2, 10=7, 11=3, 12=10, 13=!12, 14=4] [x5, !x7, 1, 6, !x3, 2, !x1, x6, x0]'),
    ('ex90', 'ex71', '[1=!4, 2=7, 3=!8, 4=6, 5=!0, 6=3, 7=!1] [7, x0, 9, 3, !7, x5, 0, 10, 6, 1, !2, 1, 2, 8, !x7, !1]'),
    ('ex91', 'ex64', '[0=!12, 1=9, 2=5, 5=!8, 7=1, 8=!4, 9=2, 10=!7, 11=10, 12=0, 13=!14, 14=!3] [!x8, x3, !x6, 2, !0, !3, !x4]'),
    ('ex92', 'ex63', '[0=3, 1=1, 2=10, 4=5, 5=!6, 6=7, 8=8, 9=!9, 10=!0, 11=11] [6, 10, 16, !5, 14, 0, 16, 5, !12, !11, 10, !4, x3, !16, x10, x7, !7]'),
    ('ex93', 'ex08', '[0=8, 1=5, 3=6, 4=15, 5=!9, 6=!4, 7=3, 8=!14, 9=!12, 10=!13, 12=7, 14=1] [x13, x11, 4, !x2]'),
    ('ex94', 'ex14', '[1=0, 2=!3, 3=!2, 4=!4, 5=1] [5, !x0, 1, 7, !7, 8, !x5, !7, 3, !7, !0, !6, 4]'),
    ('ex95', 'ex31', '[0=!14, 1=4, 2=8, 3=!11, 4=15, 5=!6, 6=!5, 7=!9, 8=3, 9=1, 10=12, 11=!13, 12=7, 13=!0, 14=!10, 15=!2] [!x8, !3, 29, x2, !49, 6, 40, !x11, !22, !37, 12, 9, !21, !x2, !7, !23, 39, !32, 27, !41, !45, x10, 7, !38, 4, !49, 47, 41, !20, !25, !28, 36, 2, 38, 46, 43, !48, !x11, !8, !6, !36, 10, 35, x8, !x1, 2, x9, !24, 3, !15, 9, 17, 33, !13, !18, x8, !x0, 16, 26, !19]'),
    ('ex96', 'ex34', '[0=!4, 1=!1, 2=!2, 3=9, 4=11, 5=14, 6=12, 7=5, 8=0, 9=10, 12=!3, 14=!15] [6, 3, 9, !1, !9, 16, x13, !2, !x11, !x10, !16, !15, 0, !17, 4, !4, 10]'),
    ('ex97', 'ex88', '[0=5, 1=!9, 2=!4, 5=12, 7=11, 8=!0, 9=10, 10=2, 11=!8, 12=1, 13=!3, 14=!13] [!x8, x3, !x6, 1, 3, !2, !x4]'),
    ('ex98', 'ex72', '[0=!8, 1=5, 2=10, 5=9, 7=14, 8=2, 9=!6, 10=7, 11=!12, 12=0, 13=!1, 14=!11] [!x8, x3, !x6, !5, !4, !3, !x4]'),
    ('ex99', 'ex13', '[0=1, 1=0, 3=2, 4=7, 5=!5, 6=6, 7=!3] [1, !0, !x2, !2]'),
]

#aig
# fastest = {
#     'ex00': 'google',
#     'ex01': 'google',
#     'ex02': 'google',
#     'ex03': 'google',
#     'ex04': 'tuw',
#     'ex05': 'google',
#     'ex06': 'tuw',
#     'ex07': 'epfl',
#     'ex08': 'google',
#     'ex09': 'tuw',
#     'ex10': 'google',
#     'ex11': 'google',
#     'ex12': 'tuw',
#     'ex13': 'google',
#     'ex14': 'tuw',
#     'ex15': 'epfl',
#     'ex16': 'google',
#     'ex17': 'tuw',
#     'ex18': 'google',
#     'ex19': 'google',
#     'ex20': 'google',
#     'ex21': 'google',
#     'ex22': 'epfl',
#     'ex23': 'google',
#     'ex24': 'tuw',
#     'ex25': 'google',
#     'ex26': 'google',
#     'ex27': 'google',
#     'ex28': 'google',
#     'ex29': 'google',
#     'ex30': 'google',
#     'ex31': 'tuw',
#     'ex32': 'tuw',
#     'ex33': 'google',
#     'ex34': 'google',
#     'ex35': 'tuw',
#     'ex36': 'google',
#     'ex37': 'google',
#     'ex38': 'google',
#     'ex39': 'tuw',
#     'ex40': 'tuw',
#     'ex41': 'tuw',
#     'ex42': 'tuw',
#     'ex43': 'google',
#     'ex44': 'google',
#     'ex45': 'google',
#     'ex46': 'tuw',
#     'ex47': 'google',
#     'ex48': 'google',
#     'ex49': 'tuw',
#     'ex50': 'google',
#     'ex51': 'google',
#     'ex52': 'tuw',
#     'ex53': 'tuw',
#     'ex54': 'google',
#     'ex55': 'google',
#     'ex56': 'tuw',
#     'ex57': 'tuw',
#     'ex58': 'google',
#     'ex59': 'google',
#     'ex60': 'google',
#     'ex61': 'google',
#     'ex62': 'google',
#     'ex63': 'google',
#     'ex64': 'google',
#     'ex65': 'tuw',
#     'ex66': 'google',
#     'ex67': 'google',
#     'ex68': 'google',
#     'ex69': 'tuw',
#     'ex70': 'google',
#     'ex71': 'tuw',
#     'ex72': 'google',
#     'ex73': 'google',
#     'ex74': 'google',
#     'ex75': 'google',
#     'ex76': 'google',
#     'ex77': 'google',
#     'ex78': 'google',
#     'ex79': 'google',
#     'ex80': 'google',
#     'ex81': 'google',
#     'ex82': 'google',
#     'ex83': 'google',
#     'ex84': 'google',
#     'ex85': 'google',
#     'ex86': 'google',
#     'ex87': 'google',
#     'ex88': 'google',
#     'ex89': 'tuw',
#     'ex90': 'google',
#     'ex91': 'tuw',
#     'ex92': 'google',
#     'ex93': 'tuw',
#     'ex94': 'tuw',
#     'ex95': 'google',
#     'ex96': 'google',
#     'ex97': 'google',
#     'ex98': 'tuw',
#     'ex99': 'google',
# }

fastest = {
    'ex00': 'google',
    'ex01': 'google',
    'ex02': 'google',
    'ex03': 'google',
    'ex04': 'tuw',
    'ex05': 'google',
    'ex06': 'tuw',
    'ex07': 'epfl',
    'ex08': 'epfl',
    'ex09': 'tuw',
    'ex10': 'google',
    'ex11': 'google',
    'ex12': 'tuw',
    'ex13': 'google',
    'ex14': 'tuw',
    'ex15': 'epfl',
    'ex16': 'google',
    'ex17': 'tuw',
    'ex18': 'google',
    'ex19': 'google',
    'ex20': 'google',
    'ex21': 'google',
    'ex22': 'google',
    'ex23': 'google',
    'ex24': 'tuw',
    'ex25': 'google',
    'ex26': 'google',
    'ex27': 'google',
    'ex28': 'google',
    'ex29': 'google',
    'ex30': 'google',
    'ex31': 'tuw',
    'ex32': 'google',
    'ex33': 'google',
    'ex34': 'google',
    'ex35': 'tuw',
    'ex36': 'google',
    'ex37': 'google',
    'ex38': 'google',
    'ex39': 'tuw',
    'ex40': 'tuw',
    'ex41': 'tuw',
    'ex42': 'tuw',
    'ex43': 'google',
    'ex44': 'google',
    'ex45': 'google',
    'ex46': 'tuw',
    'ex47': 'google',
    'ex48': 'google',
    'ex49': 'tuw',
    'ex50': 'google',
    'ex51': 'google',
    'ex52': 'tuw',
    'ex53': 'tuw',
    'ex54': 'google',
    'ex55': 'tuw',
    'ex56': 'tuw',
    'ex57': 'tuw',
    'ex58': 'google',
    'ex59': 'google',
    'ex60': 'google',
    'ex61': 'tuw',
    'ex62': 'google',
    'ex63': 'tuw',
    'ex64': 'google',
    'ex65': 'tuw',
    'ex66': 'google',
    'ex67': 'google',
    'ex68': 'google',
    'ex69': 'tuw',
    'ex70': 'google',
    'ex71': 'tuw',
    'ex72': 'google',
    'ex73': 'tuw',
    'ex74': 'google',
    'ex75': 'google',
    'ex76': 'google',
    'ex77': 'google',
    'ex78': 'google',
    'ex79': 'google',
    'ex80': 'google',
    'ex81': 'google',
    'ex82': 'google',
    'ex83': 'google',
    'ex84': 'google',
    'ex85': 'google',
    'ex86': 'google',
    'ex87': 'google',
    'ex88': 'google',
    'ex89': 'tuw',
    'ex90': 'google',
    'ex91': 'tuw',
    'ex92': 'google',
    'ex93': 'google',
    'ex94': 'tuw',
    'ex95': 'google',
    'ex96': 'google',
    'ex97': 'tuw',
    'ex98': 'tuw',
    'ex99': 'tuw',
}


def produce(orig_bench, new_bench, substitution, outs):
    with open(orig_bench) as file:
        lines = [line.rstrip() for line in file]
        inputs = []
        outputs = []
        buffs = []
        main = []
        names = []
        inv_suffix = '_inv'
        fictitious_suffix = '_fictitious'
        fictitious_index = 0
        for line in lines:
            input_pattern = r'INPUT\((.*?)\)'
            input_result = re.search(input_pattern, line)
            if input_result:
                input_name = input_result.group(1)
                inputs.append(input_name)
            else:
                output_pattern = r'OUTPUT\((.*?)\)'
                output_result = re.search(output_pattern, line)
                if output_result:
                    output_name = output_result.group(1)
                    outputs.append(output_name)
                else:
                    main.append(line)
        new_inputs = []
        nots = []
        for k in sorted(substitution.keys()):
            v, n = substitution[k]
            if not n:
                new_inputs.append(inputs[v])
            else:
                inv_name = inputs[v] + inv_suffix
                new_inputs.append(inv_name)
                names.append(inputs[v])
                nots.append((inputs[v], inv_name))

        sorted_outs = sorted(filter(lambda x: x[0] == 'in', outs), key=lambda x: x[1], reverse=False)

        fictitious_vars = {}

        for s, idx, neg in sorted_outs:
            # Такая фиктивная переменная уже существует
            if (idx, neg) in fictitious_vars:
                continue
            # Фиктивная переменная существует
            if (idx, False) in fictitious_vars:
                # Надо проинвертировать
                if neg:
                    name = fictitious_vars[(idx, False)]
                    if (idx, True) in fictitious_vars:
                        continue
                    inv_name = name + inv_suffix
                    names.append(inv_name)
                    fictitious_vars[(idx, True)] = inv_name
                    nots.append((inv_name, name))
                continue
            # Фиктивная переменная уже существует, раз есть её отрицание
            if (idx, True) in fictitious_vars:
                continue
            if idx in substitution:
                fictitious_vars[(idx, False)] = new_inputs[idx]
                if neg:
                    # Если переменная уже проинвертирована, надо взять оригинал
                    if new_inputs[idx].endswith(inv_suffix):
                        fictitious_vars[(idx, True)] = new_inputs[idx][:-len(inv_suffix)]
                    else:
                        inv_name = new_inputs[idx] + inv_suffix
                        fictitious_vars[(idx, True)] = inv_name
                        names.append(inv_name)
                        inv = (inv_name, new_inputs[idx])
                        nots.append(inv)
                continue
            fictitious_name = str(fictitious_index) + fictitious_suffix
            fictitious_index += 1
            fictitious_vars[(idx, False)] = fictitious_name
            new_inputs.insert(idx, fictitious_name)
            if neg:
                inv_name = fictitious_name + inv_suffix
                inv = (inv_name, fictitious_name)
                names.append(inv_name)
                if inv not in nots:
                    nots.append(inv)
                fictitious_vars[(idx, True)] = inv_name

        new_outputs = []
        for s, idx, neg in outs:
            if s == 'in':
                name = fictitious_vars[(idx, neg == 1)]
                b = False
                while name in new_outputs:
                    name += "_buff"
                    b = True
                if b:
                    buffs.append((name, fictitious_vars[(idx, neg == 1)]))
                names.append(name)
                new_outputs.append(name)
            else:
                if not neg:
                    name = outputs[idx]
                    b = False
                    while name in new_outputs:
                        name += "_buff"
                        b = True
                    if b:
                        buffs.append((name, outputs[idx]))
                    names.append(name)
                    new_outputs.append(name)
                else:
                    print(idx)
                    inv_name = outputs[idx] + inv_suffix
                    name = inv_name
                    b = False
                    while name in new_outputs:
                        name += "_buff"
                        b = True
                    if b:
                        buffs.append((name, inv_name))
                    new_outputs.append(name)
                    names.append(name)
                    names.append(outputs[idx])
                    inv = (inv_name, outputs[idx])
                    if inv not in nots:
                        nots.append(inv)

        index = 0
        print(names)
        while True:
            index += 1
            changed = False
            new_lines = []
            lefts = []
            rs = set()
            ls = []
            for line in main:
                if line == '\n' or line == '' or line == '\r\n':
                    continue
                line = line.replace(' ', '')
                #print(line, line.index('='))
                left = line[:line.index('=')]
                rights = line[line.index('(') + 1:line.index(')')].split(',')
                for right in rights:
                    rs.add(right)
                ls.append(left)
            for left in ls:
                if left not in rs and left not in new_outputs and left not in names:
                    #print(left)
                    changed = True
                    continue
                lefts.append(left)
            for line in main:
                if line == '\n' or line == '' or line == '\r\n':
                    continue
                line = line.replace(' ', '')
                #print(f'({line})')
                left = line[:line.index('=')]
                if left not in lefts:
                    changed = True
                    continue
                rights = line[line.index('(') + 1:line.index(')')].split(',')
                can = True
                for right in rights:
                    if right not in lefts and right not in new_inputs and right not in names:
                        changed = True
                        can = False
                        break
                if can:
                    new_lines.append(line)

            if not changed:
                break

            main = new_lines

        with open(new_bench, 'w') as f:
            for _input in new_inputs:
                f.write(f'INPUT({_input})\n')
            f.write('\n')
            for v1, v2 in nots:
                f.write(f'{v1}=NOT({v2})\n')
            f.write('\n')
            for line in main:
                f.write(line + '\n')
            f.write('\n')
            for v1, v2 in buffs:
                f.write(f'{v1}=BUFF({v2})\n')
            f.write('\n')
            for output in new_outputs:
                f.write(f'OUTPUT({output})\n')

preffix = '../../../mnt/d/education/bench/lal/circuit-synthesis/'


if os.path.exists(preffix + 'iwls2024/best_from_2023/xaig_bench'):
    shutil.rmtree(preffix + 'iwls2024/best_from_2023/xaig_bench')


substitution = {}
outs = []

sub_str = '0=3, 1=6, 2=10, 3=!0, 4=!5, 5=!1, 6=!8, 7=!9, 8=!2'.split(', ')
#sub_str = '0=11, 1=!3, 2=!9, 5=5, 7=8, 8=!7, 9=!0, 10=!6, 11=4, 12=!10, 13=!2, 14=!1'.split(', ')
outs_str = '0'.split(', ')
#outs_str = '!x8, x3, !x6, 4, !0, 2, !x4'.split(', ')
for sub in sub_str:
    print(sub)
    fst = int(sub[:sub.find('=')])
    snd = sub[sub.find('=')+1:]
    neg = 0
    if snd[0] == '!':
        neg = 1
        snd = snd[1:]
    snd_int = int(snd)
    substitution[fst] = (snd_int, neg)
for out in outs_str:
    neg = 0
    if out[0] == '!':
        neg = 1
        out = out[1:]
    s = 'out'
    if out[0] == 'x':
        s = 'in'
        out = out[1:]
    out_int = int(out)
    outs.append((s, out_int, neg))

produce('ex57.bench', 'google_maj.bench', substitution, outs)



# for file1, file2, sub_and_outs in info:
#     #if file1 != 'ex00':
#     #    continue
#     print(f'processing {file1}')
#     comp = fastest[file2]
#     filename = f'{file1}_from_{file2}_{comp}.bench'
#     new_path = preffix + f'iwls2024/best_from_2023/xaig_bench/' + filename
#     if not os.path.exists(preffix + 'iwls2024/best_from_2023/xaig_bench'):
#         os.makedirs(preffix + '/iwls2024/best_from_2023/xaig_bench')
#     old_path = preffix + f'iwls2023/submissions/{comp}/xaig_bench/{file2}.bench'
#     substitution = {}
#     outs = []
#     sub_str = sub_and_outs[1:sub_and_outs.find(']')].split(', ')
#     outs_str = sub_and_outs[sub_and_outs.find(']') + 3:-1].split(', ')
#     for sub in sub_str:
#         fst = int(sub[:sub.find('=')])
#         snd = sub[sub.find('=')+1:]
#         neg = 0
#         if snd[0] == '!':
#             neg = 1
#             snd = snd[1:]
#         snd_int = int(snd)
#         substitution[fst] = (snd_int, neg)
#     for out in outs_str:
#         neg = 0
#         if out[0] == '!':
#             neg = 1
#             out = out[1:]
#         s = 'out'
#         if out[0] == 'x':
#             s = 'in'
#             out = out[1:]
#         out_int = int(out)
#         outs.append((s, out_int, neg))
#     produce(old_path, new_path, substitution, outs)
#     print(new_path)
#     output = subprocess.run([
#         'python3',
#         preffix + 'scripts/cli.py',
#         'verify',
#         preffix + f'iwls2024/truth_tables/{file1}.truth',
#         new_path
#     ], capture_output=True).stdout.decode('utf-8')
#     #assert "Networks are equivalent" in output
#     if "Networks are equivalent" not in output:
#         print('problem')
#         print(output)
#         continue
#
#     patt = 'AND-gates: '
#
#     size1_out = subprocess.run([
#         'python3',
#         preffix + 'scripts/cli.py',
#         'get-size',
#         preffix + f'iwls2023/submissions/{comp}/xaig/{file2}.aig'
#     ], capture_output=True).stdout.decode('utf-8')
#     size1 = int(size1_out[size1_out.find(patt) + len(patt):].strip().split('.')[0])
#
#     size2_out = subprocess.run([
#         'python3',
#         preffix + 'scripts/cli.py',
#         'get-size',
#         new_path
#     ], capture_output=True).stdout.decode('utf-8')
#     size2 = int(size2_out[size2_out.find(patt) + len(patt):].strip().split('.')[0])
#
#     print(f'old size: {size1}; new size: {size2}')
