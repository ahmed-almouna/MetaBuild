'use client';
import Image from "next/image";
import styles from "@/ui/page.module.css";
import  BuildButton from "@/ui/app/build-button";
import  BudgetSlider from "@/ui/app/budget-slider";
import PurposeRadios from "@/ui/app/purpose-radios";
import ResolutionRadios from "@/ui/app/resolution-radios";
import FeaturesCheckboxes from "@/ui/app/features-checkboxes";
import { Content } from "next/font/google";
import { handleSubmit } from "@/common/utlis";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>

        <h1 className="text-center display-6 fw-bold mb-4">MetaBuild PC Builder</h1>

        <form style={{display: 'contents'}} onSubmit={handleSubmit}>
          <BudgetSlider />
          <PurposeRadios />
          <ResolutionRadios />
          <FeaturesCheckboxes />
          <BuildButton />
        </form>


  


      </main>
      {/* <footer className={styles.footer}>
        
      </footer> */}
    </div>
  );
}
