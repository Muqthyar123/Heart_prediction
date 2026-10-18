import { motion, useReducedMotion } from "framer-motion";
import heartSapphire from "@/assets/heart-sapphire.jpg";

/** Hero heart image blended directly into the page background. Decorative. */
export function HeartVisual() {
  const reduce = useReducedMotion();
  return (
    <div className="hero-visual relative mx-auto aspect-square w-full max-w-[320px] sm:max-w-[600px]" aria-hidden>
      <motion.img
        src={heartSapphire}
        width={1200}
        height={1200}
        alt=""
        className="hero-blend absolute inset-0 size-full object-cover"
        animate={reduce ? false : { scale: [1, 1.015, 1] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      />
    </div>
  );
}
