`gtime` uses the same output mapping as `gnu`, so it is omitted here.
The normalized cross-platform mapping below is intended to keep output field
names and intended semantics consistent across backends, not to claim exact
kernel-level equivalence between GNU and BSD/macOS counters.

| TSV column / feature | gnu<sup><a href="#cmd-a">a</a></sup> | bsd<sup><a href="#cmd-b">b</a></sup> |
|---|---|---|
| execution | see <sup><a href="#cmd-a">a</a></sup> | see <sup><a href="#cmd-b">b</a></sup> |
| * `experiment` | galitime field from `-n/--name` | galitime field from `-n/--name` |
| * `run` | galitime repetition index | galitime repetition index |
| * `real_s` | `%e` | `real` |
| * `user_s` | `%U` | `user` |
| * `sys_s` | `%S` | `sys` |
| * `cpu_s` | `user_s + sys_s` | `user_s + sys_s` |
| * `cpu_pct` | `100 * cpu_s / real_s` | `100 * cpu_s / real_s` |
| * `max_ram_kb` | `%M` – normalized from KiB to kB | `maximum resident set size` – normalized from bytes to kB |
| `backend` | `"gnu"` | `"bsd"` |
| `fs_input_ops` | `%I` | `block input operations` |
| `fs_output_ops` | `%O` | `block output operations` |
| `major_page_faults` | `%F` | `page faults` |
| `minor_page_faults` | `%R` | `page reclaims` (BSD/macOS label mapped to the normalized cross-platform field name) |
| `swaps` | `%W` | `swaps` |
| * `status` | derived from `exit_code` | derived from `exit_code` |
| * `exit_code` | shell `EXIT` trap | shell `EXIT` trap |
| * `command` | galitime logged command string | galitime logged command string |

<a id="cmd-a"></a>
**a:**
```bash
/usr/bin/env time -o <tmp> -f "%e\t%U\t%S\t%P\t%M\t%I\t%O\t%F\t%R\t%W" <shell> -c <command_script>
```

<a id="cmd-b"></a>
**b:**
```bash
/usr/bin/env time -o <tmp> -l -p <shell> -c <command_script>
```
