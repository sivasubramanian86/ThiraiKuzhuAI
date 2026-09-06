import { describe, it, expect } from "vitest";
import { LOCALES } from "../i18n/index.js";
import { en } from "../i18n/locales/en.js";
import { ta } from "../i18n/locales/ta.js";
import { hi } from "../i18n/locales/hi.js";
import { ja } from "../i18n/locales/ja.js";

describe("i18n Locales & Translation Coverage", () => {
  it("should contain all required language definitions in LOCALES", () => {
    const requiredCodes = ["en", "ta", "hi", "te", "ml", "ja", "ko", "zh", "fr"];
    for (const code of requiredCodes) {
      expect(LOCALES).toHaveProperty(code);
      expect(LOCALES[code]).toHaveProperty("code");
      expect(LOCALES[code]).toHaveProperty("name");
      expect(LOCALES[code]).toHaveProperty("brandSubtitle");
      expect(LOCALES[code]).toHaveProperty("dispatchBtn");
      expect(LOCALES[code]).toHaveProperty("walkieTitle");
    }
  });

  it("should have correct translations for English base locale", () => {
    expect(en.code).toBe("en");
    expect(en.name).toBe("English (Global)");
    expect(en.incidentHeading).toBe("Studio Pipeline Incidents");
    expect(en.walkieTitle).toBe("Studio Walkie-Talkie (Ch 1)");
  });

  it("should have authentic Tamil film terminology in ta locale", () => {
    expect(ta.code).toBe("ta");
    expect(ta.name).toContain("தமிழ்");
    expect(ta.incidentHeading).toBe("திரைப்பட தயாரிப்பு சிக்கல்கள்");
    expect(ta.walkieTitle).toContain("படப்பிடிப்பு வாக்கி-டாக்கி");
  });

  it("should have complete Hindi translations in hi locale", () => {
    expect(hi.code).toBe("hi");
    expect(hi.name).toContain("हिन्दी");
    expect(hi.incidentHeading).toBe("स्टूडियो पाइपलाइन घटनाएं");
  });

  it("should have Japanese cinema terms in ja locale", () => {
    expect(ja.code).toBe("ja");
    expect(ja.name).toContain("日本語");
    expect(ja.incidentHeading).toBe("スタジオ制作インシデント");
  });
});
