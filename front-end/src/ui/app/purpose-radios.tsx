import React from 'react';
import styles from "@/ui/page.module.css";

export default function PurposeRadios() {
    return (
        <>
            <h6 className='mt-4'>Primary Purpose</h6>
            <div className="row mx-0 gap-4"> 

                <label htmlFor="purpose_gaming" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Purpose" value="Gaming" id="purpose_gaming" defaultChecked style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Gaming</h6>
                            <p className="mb-0 text-muted">High FPS, smooth gameplay</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="purpose_streaming" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Purpose" value="Streaming" id="purpose_streaming" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Content Creation</h6>
                            <p className="mb-0 text-muted">Video editing, recording, streaming</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="purpose_working" className={`card col ${styles.purposeRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Purpose" value="Working" id="purpose_working" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">Productivity</h6>
                            <p className="mb-0 text-muted">Multi-tasking, 3D rendering, animation</p>
                        </div>  
                    </div>
                </label>

            </div>
        </>
    );
}