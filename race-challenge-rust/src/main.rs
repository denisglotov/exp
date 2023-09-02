use anyhow;

struct Counter(u64);

impl Counter {
    async fn race(&mut self) {
        for _ in 0..1_000_000 {
            self.0 += 1;
        }
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut cnt = Counter(0);
    tokio::join! {cnt.race(), cnt.race()};
    println!("{}", cnt.0);
    Ok(())
}
