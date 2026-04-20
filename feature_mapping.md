# Galitime feature mapping

| TSV column / feature | gnu<sup>a</sup> | gtime<sup>b</sup> | bsd<sup>c</sup> |
|---|---|---|---|
| execution | see <sup>a</sup> | see <sup>b</sup> | see <sup>c</sup> |
| * `experiment` | galitime field from `-n/--name` | galitime field from `-n/--name` | galitime field from `-n/--name` |
| * `run` | galitime repetition index | galitime repetition index | galitime repetition index |
| * `real_s` | `%e` | `%e` | `real` |
| * `user_s` | `%U` | `%U` | `user` |
| * `sys_s` | `%S` | `%S` | `sys` |
| * `cpu_s` | `user_s + sys_s` | `user_s + sys_s` | `user_s + sys_s` |
| * `cpu_pct` | `100 * cpu_s / real_s` | `100 * cpu_s / real_s` | `100 * cpu_s / real_s` |
| * `max_ram_kb` | `%M` – normalized from KiB to kB | `%M` – normalized from KiB to kB | `maximum resident set size` – normalized from bytes to kB |
| `backend` | `"gnu"` | `"gtime"` | `"bsd"` |
| `fs_inputs` | `%I` | `%I` | `block input operations` |
| `fs_outputs` | `%O` | `%O` | `block output operations` |
| `major_page_faults` | `%F` | `%F` | `page faults` |
| `minor_page_faults` | `%R` | `%R` | `page reclaims` |
| `swaps` | `%W` | `%W` | `swaps` |
| * `status` | derived from `exit_code` | derived from `exit_code` | derived from `exit_code` |
| * `exit_code` | shell `EXIT` trap | shell `EXIT` trap | shell `EXIT` trap |
| * `command` | galitime logged command string | galitime logged command string | galitime logged command string |

[^a]: `/usr/bin/env time -o <tmp> -f "%e\t%U\t%S\t%P\t%M\t%I\t%O\t%F\t%R\t%W" <shell> -c <command_script>`
[^b]: `/usr/bin/env gtime -o <tmp> -f "%e\t%U\t%S\t%P\t%M\t%I\t%O\t%F\t%R\t%W" <shell> -c <command_script>`
[^c]: `/usr/bin/env time -o <tmp> -l -p <shell> -c <command_script>`