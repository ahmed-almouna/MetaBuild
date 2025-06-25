import React from 'react';
import styles from "@/ui/page.module.css";

export default function ResolutionRadios() {
    return (
        <>
            <h6 className='mt-4'>Resolution</h6>
            <div className="row mx-0 gap-4"> 

                <label htmlFor="resolution_1080p" className={`card col-auto flex-grow-1  ${styles.resolutionRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Resolution" value="1080p" id="resolution_1080p" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">1080p</h6>
                            <p className="mb-0 text-muted">Full HD, High refresh rate</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="resolution_1440p" className={`card col-auto flex-grow-1 ${styles.resolutionRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Resolution" value="1440p" id="resolution_1440p" defaultChecked style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">1440p</h6>
                            <p className="mb-0 text-muted">2K, Balanced</p>
                        </div>  
                    </div>
                </label>

                <label htmlFor="resolution_2160p" className={`card col-auto flex-grow-1 ${styles.resolutionRadioCard}`}>
                    <div className="card-body row align-items-center">
                        <div className="form-check col-auto">
                            <input className="form-check-input" type="radio" name="Resolution" value="2160p" id="resolution_2160p" style={{cursor: 'pointer'}}/>
                        </div>
                
                        <div className="col-auto">
                            <h6 className="mb-1">2160p</h6>
                            <p className="mb-0 text-muted">4K, High setting visuals</p>
                        </div>  
                    </div>
                </label>
            </div>
        </>
    );
}