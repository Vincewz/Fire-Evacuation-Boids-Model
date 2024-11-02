# main.py
import argparse
from simulation import SimulationRecorder

def parse_args():
    parser = argparse.ArgumentParser(description='Run Boids simulation with optional video recording')
    parser.add_argument('--record', '-r', action='store_true',
                      help='Start recording automatically')
    parser.add_argument('--output', '-o', type=str, default='simulation_recording.mp4',
                      help='Output video filename (default: simulation_recording.mp4)')
    parser.add_argument('--fps', type=int, default=30,
                      help='Recording framerate (default: 30)')
    parser.add_argument('--duration', '-d', type=int,
                      help='Recording duration in seconds (optional)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sim = SimulationRecorder(record_fps=args.fps)
    
    if args.record:
        sim.start_recording(args.output)
        
        if args.duration:
            # Si une durée est spécifiée, on lance la simulation pour cette durée
            sim.run(max_frames=args.duration * args.fps)
        else:
            # Sinon, on lance la simulation normalement
            sim.run()
    else:
        sim.run()