use sha3::{Digest, Keccak256};
use std::env;

const SIZE: usize = 32;

fn main() {
    let mut data = [0u8; SIZE];
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 {
        hex::decode_to_slice(&args[1], &mut data).unwrap();
    }

    let (mut step, mut found) = (0, 0);
    loop {
        let mut hasher = Keccak256::new();
        hasher.update(&data);
        let hash = hasher.finalize();

        if hash[0] == 0xbe && hash[1] == 0xce && hash[2] == 0xd0 && hash[3] == 0x95 {
            println!("MATCH1 on {step}: {}", hex::encode(&data));
            found |= 1;
        }

        if hash[0] == 0x42 && hash[1] == 0xa7 && hash[2] == 0xb7 && hash[3] == 0xdd {
            println!("MATCH2 on {step}: {}", hex::encode(&data));
            found |= 2;
        }

        if hash[0] == 0x45 && hash[1] == 0xe0 && hash[2] == 0x10 && hash[3] == 0xb9 {
            println!("MATCH3 on {step}: {}", hex::encode(&data));
            found |= 4;
        }

        if hash[0] == 0xa8 && hash[1] == 0x6c && hash[2] == 0x33 && hash[3] == 0x9e {
            println!("MATCH4 on {step}: {}", hex::encode(&data));
            found |= 8;
        }

        if found == 15 {
            break;
        }

        for j in (0..SIZE).rev() {
            data[j] = data[j].wrapping_add(1);
            if data[j] != 0 {
                break;
            }
        }
        step += 1;
        if step % 500000 == 0 {
            eprintln!("{found}@{step}: {}", hex::encode(&data));
        }
    }
}
