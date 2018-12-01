// Advent of Code 2018, Day 1
// (c) blu3r4y

use std::fs;
use std::collections::HashSet;

fn part1(arr: &Vec<i32>) -> i32 {
    return arr.iter().sum();
}

fn part2(arr: &Vec<i32>) -> i32 {
    let mut frequency = 0;
    let mut seen = HashSet::new();

    seen.insert(0);

    for e in arr.iter().cycle() {
        frequency += e;
        if seen.contains(&frequency) {
            return frequency;
        }
        seen.insert(frequency);
    }

    return -1;
}

fn main() {
    let arr: Vec<i32> = fs::read_to_string("assets/day1.txt").unwrap()
        .lines()
        .map(|line| line.parse::<i32>().unwrap())
        .collect();

    println!("{}", part1(&arr));
    println!("{}", part2(&arr));
}
