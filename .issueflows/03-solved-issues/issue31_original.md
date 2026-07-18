# Issue #31: Materialize filter_local results to a list

Source: https://github.com/ife-bat/oeleo/issues/31

## Original issue text

## Summary
`filter_local` may leave a generator in `Worker.file_names`. `run` consumes it once; a second `run` without re-filter sees an empty iterable. `add_local` already warns about generators; `filter_local` should always materialize.

**Finding ID:** REL-03  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Fix direction
Materialize to `list` at the end of `filter_local` (and keep `file_names` as a list thereafter).

## Acceptance
- [ ] `filter_local` leaves `file_names` as a `list`
- [ ] Second `run()` without re-filter still sees the same files
- [ ] Unit test covers double-`run` after one `filter_local`
